/* Includes ---------------------------------------------------------------- */
#include <Pegase-test-chaise-bouteille_inferencing.h>
#include "edge-impulse-sdk/dsp/image/image.hpp"

#include "camera.h"
#include "esp_camera.h"
#include "http_wifi.h"
#include "esp_heap_caps.h"

/* Constant defines -------------------------------------------------------- */
#define EI_CAMERA_RAW_FRAME_BUFFER_COLS 640
#define EI_CAMERA_RAW_FRAME_BUFFER_ROWS 480
#define EI_CAMERA_FRAME_BYTE_SIZE 3

#define EI_REZIZE_BUF_COLS 96
#define EI_REZIZE_BUF_ROWS 96
#define EI_REZIZE_FRAME_BYTE_SIZE 3

/* Private variables ------------------------------------------------------- */
static bool debug_nn = false; // Set this to true to see e.g. features generated from the raw signal
static bool is_initialised = false;
uint8_t *snapshot_buf; // points to the output of the capture
uint8_t *ei_resize_buf = nullptr;

uint8_t *debug_jpeg = nullptr; // envoi debug http
size_t debug_jpeg_len = 0;

/* Function definitions ------------------------------------------------------- */
bool ei_camera_capture(uint32_t img_width, uint32_t img_height, uint8_t *out_buf);
static int ei_camera_get_data(size_t offset, size_t length, float *out_ptr);

void initBuffers()
{
    // allocate memory for the snapshot buffer
    snapshot_buf = (uint8_t *)malloc(EI_CAMERA_RAW_FRAME_BUFFER_COLS * EI_CAMERA_RAW_FRAME_BUFFER_ROWS * EI_CAMERA_FRAME_BYTE_SIZE);

    if (snapshot_buf == nullptr)
    {
        Serial.println("ERR: Failed to allocate snapshot buffer!\n");
        return;
    }

    else
    {
        Serial.print("Adresse buffer : ");
        Serial.println((uint32_t)snapshot_buf);
    }

    ei_resize_buf = (uint8_t *)malloc(EI_REZIZE_BUF_COLS * EI_REZIZE_BUF_ROWS * EI_REZIZE_FRAME_BYTE_SIZE);

    if (ei_resize_buf == nullptr)
    {
        Serial.println("ERR: Failed to allocate resize buffer!\n");
        return;
    }
    else
    {
        Serial.print("Adresse resize buffer : ");
        Serial.println((uint32_t)ei_resize_buf);
    }
}

/**
 * @brief      Arduino setup function
 */
void setup()
{
    Serial.begin(115200);
    // comment out the below line to start inference immediately after upload
    delay(3000);
    Serial.println(EI_CLASSIFIER_PROJECT_ID);
    Serial.println(EI_CLASSIFIER_PROJECT_OWNER);

    Serial.println("Edge Impulse Inferencing Demo");

    delay(1000);
    Serial0.println("Initialisation camera");
    initCamera();
    Serial0.println("Initialisation camera OK");
    initWifi();
    delay(1000);
    test_camera();
    delay(1000);
    Serial0.println("Initialisation camera et Wifi OK");
    is_initialised = true;
    initBuffers();
}

/**
 * @brief      Get data and run inferencing
 *
 * @param[in]  debug  Get debug info if true
 */
void loop()

{

    handleWifi();
    delay(50);

    // instead of wait_ms, we'll wait on the signal, this allows threads to cancel us...
    if (ei_sleep(5) != EI_IMPULSE_OK)
    {
        return;
    }

    // Serial.print("Adresse buffer : ");
    // Serial.println((uint32_t)snapshot_buf);
    // Serial.print("Adresse resize buffer : ");
    // Serial.println((uint32_t)ei_resize_buf);
    // check if allocation was successful
    if (snapshot_buf == nullptr)
    {
        Serial.println("ERR: Failed to allocate snapshot buffer!\n");
        return;
    }
    // Serial.println("BUFFER OK");

    ei::signal_t signal;
    signal.total_length = EI_CLASSIFIER_INPUT_WIDTH * EI_CLASSIFIER_INPUT_HEIGHT;
    signal.get_data = &ei_camera_get_data;

    if (ei_camera_capture((size_t)EI_CLASSIFIER_INPUT_WIDTH, (size_t)EI_CLASSIFIER_INPUT_HEIGHT, snapshot_buf) == false)
    {
        Serial.println("Failed to capture image\r\n");
        free(snapshot_buf);
        return;
    }
    // Run the classifier
    ei_impulse_result_t result = {0};

    EI_IMPULSE_ERROR err = run_classifier(&signal, &result, debug_nn);
    if (err != EI_IMPULSE_OK)
    {
        Serial.printf("ERR: Failed to run classifier (%d)\n", err);
        return;
    }
    // Serial.println("IMAGE OK");
    // print the predictions
    Serial.printf("Predictions (DSP: %d ms., Classification: %d ms., Anomaly: %d ms.): \n",
                  result.timing.dsp, result.timing.classification, result.timing.anomaly);
    // Serial.println("PREDICTIONS OK");

    // Serial.println("Bounding boxes:");
    // for (uint32_t i = 0; i < result.bounding_boxes_count; i++)
    // {
    //     ei_impulse_result_bounding_box_t bb = result.bounding_boxes[i];
    //     if (bb.value == 0)
    //     {
    //         continue;
    //     }
    //     Serial.printf("  %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\r\n",
    //               bb.label,
    //               bb.value,
    //               bb.x,
    //               bb.y,
    //               bb.width,
    //               bb.height);
    // }

    // Print the prediction results (classification)

    Serial.println("Predictions:");
    float scoreBouteille = 0.0;
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++)
    {
        Serial.printf("  %s: ", ei_classifier_inferencing_categories[i]);
        Serial.printf("%.5f\r\n", result.classification[i].value);

        if (strcmp(ei_classifier_inferencing_categories[i], "Bouteille") == 0)
        {
            scoreBouteille = result.classification[i].value;
        }
    }

        if(scoreBouteille > 0.60)
        {
            Serial.println("Bouteille détectée");
            envoyerSiDetection("bouteille", scoreBouteille);
        }
        else
        {
            Serial.println("Pas de bouteille détectée");
        }


    // Print anomaly result (if it exists)
#if EI_CLASSIFIER_HAS_ANOMALY
    Serial.printf("Anomaly prediction: %.3f\r\n", result.anomaly);
#endif

#if EI_CLASSIFIER_HAS_VISUAL_ANOMALY
    Serial.printf("Visual anomalies:\r\n");
    for (uint32_t i = 0; i < result.visual_ad_count; i++)
    {
        ei_impulse_result_bounding_box_t bb = result.visual_ad_grid_cells[i];
        if (bb.value == 0)
        {
            continue;
        }
        Serial.printf("  %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\r\n",
                      bb.label,
                      bb.value,
                      bb.x,
                      bb.y,
                      bb.width,
                      bb.height);
    }
#endif
}

/**
 * @brief   Setup image sensor & start streaming
 *
 * @retval  false if initialisation failed
 */

bool ei_camera_capture(uint32_t img_width, uint32_t img_height, uint8_t *out_buf)
{
    bool do_resize = false;
    if (!is_initialised)
    {
        Serial.println("ERR: Camera is not initialized\r\n");
        return false;
    }

    camera_fb_t *fb = esp_camera_fb_get();

    if (!fb)
    {
        Serial.println("Camera capture failed\n");
        Serial.println("C");

        return false;
    }
    // Serial.print("Image : ");

    // Serial.print(fb->width);
    // Serial.print("x");
    // Serial.println(fb->height);

    // Serial.print("Taille JPEG : ");
    // Serial.print(fb->len);
    // Serial.println(" octets");

    bool converted = fmt2rgb888(fb->buf, fb->len, PIXFORMAT_JPEG, snapshot_buf);

    // Serial.print("CONVERTI : ");
    // Serial.println(converted);

    // Serial.print("EI INPUT : ");
    // Serial.print(img_width);
    // Serial.print("x");
    // Serial.println(img_height);

    // Serial.print("RAW BUFFER : ");
    // Serial.print(EI_CAMERA_RAW_FRAME_BUFFER_COLS);
    // Serial.print("x");
    // Serial.println(EI_CAMERA_RAW_FRAME_BUFFER_ROWS);

    esp_camera_fb_return(fb);

    if (!converted)
    {
        Serial.printf("Conversion failed\n");
        return false;
    }

    if ((img_width != EI_CAMERA_RAW_FRAME_BUFFER_COLS) || (img_height != EI_CAMERA_RAW_FRAME_BUFFER_ROWS))
    {
        do_resize = true;
    }

    // Serial.print("DO RESIZE : ");
    // Serial.println(do_resize);

    if (do_resize)
    {
        ei::image::processing::crop_and_interpolate_rgb888(
            snapshot_buf,
            EI_CAMERA_RAW_FRAME_BUFFER_COLS,
            EI_CAMERA_RAW_FRAME_BUFFER_ROWS,
            out_buf,
            img_width,
            img_height);
    }

    ei_resize_buf = out_buf;
    /*DEBUG*/
    // Serial.print("PIXEL RESIZE : ");
    // Serial.print(out_buf[0]);
    // Serial.print(" ");
    // Serial.print(out_buf[1]);
    // Serial.print(" ");
    // Serial.println(out_buf[2]);
    // copie de debug de l'image réellement envoyée à Edge Impulse
    if (debug_jpeg != nullptr)
    {
        free(debug_jpeg);
        debug_jpeg = nullptr;
    }
    // Copie de debug de l'image réellement envoyée à Edge Impulse
    fmt2jpg(
        ei_resize_buf,
        img_width * img_height * 3,
        img_width,
        img_height,
        PIXFORMAT_RGB888,
        80,
        &debug_jpeg,
        &debug_jpeg_len);

    return true;
}

static int ei_camera_get_data(size_t offset, size_t length, float *out_ptr)
{
    static bool first = true;

    // we already have a RGB888 buffer, so recalculate offset into pixel index
    size_t pixel_ix = offset * 3;
    size_t pixels_left = length;
    size_t out_ptr_ix = 0;

    while (pixels_left != 0)
    {
        // Swap BGR to RGB here
        // due to https://github.com/espressif/esp32-camera/issues/379
        out_ptr[out_ptr_ix] = (ei_resize_buf[pixel_ix + 2] << 16) + (ei_resize_buf[pixel_ix + 1] << 8) + ei_resize_buf[pixel_ix];

        if (first)
        {
            Serial.print("OFFSET : ");
            Serial.println(offset);
            Serial.print("LENGTH : ");
            Serial.println(length);
            Serial.print("PIXEL 0 : ");
            Serial.println(out_ptr[0]);
            first = false;
        }

        // go to the next pixel
        out_ptr_ix++;
        pixel_ix += 3;
        pixels_left--;
    }
    // and done!
    return 0;
}

#if !defined(EI_CLASSIFIER_SENSOR) || EI_CLASSIFIER_SENSOR != EI_CLASSIFIER_SENSOR_CAMERA
#error "Invalid model for current sensor"
#endif
