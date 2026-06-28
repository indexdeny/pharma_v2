# RPA BROWSER RENDER LOOP VALIDATION

This document summarizes the validation of the Selenium RPA render loop in `gemini_image_generator.py` and details the stability measures, timing constraints, and failure recovery behaviors.

---

## 1. SELENIUM INSTABILITY & TIMING ISSUES

Selenium automation interacting with dynamic SPA interfaces like Gemini UI is subject to latency shifts. The following stability measures have been validated:

- **Chat Input Polling**: Gemini UI asynchronously renders the text input zone. The script polls a hierarchy of selectors (`div.ql-editor[contenteditable='true']`, `rich-textarea div[contenteditable='true']`, etc.) with a 20-second timeout to accommodate slow script initialization.
- **Pre-Flight Idle Wait**: Prior to sending any prompt, `wait_for_chat_idle()` checks that the Gemini send button is enabled, preventing prompt injection during loading states.
- **Post-Click Delay**: A 2-second stabilization delay (`POST_CLICK_DELAY`) is enforced before blob extraction to allow the DOM to link the blob resource to the image source element.

---

## 2. UI RACE CONDITIONS & RESPONSE DETECTION

- **Responses Counting**: Before submitting a prompt, the script records the count of responses currently in the chat container (`responses_before`). 
- **Image Generation Polling**: The script polls for new `model-response` elements. A generation is marked complete when the response count increases and the last response container contains a fully loaded `img` element with a `blob:` source.
- **Timeout Protection**: If image generation exceeds `IMAGE_GENERATION_TIMEOUT` (180 seconds), a screenshot of the browser DOM is saved (`error_gen_<stem>.png`), the failure is logged to `/render_output/failed_logs/failures.log`, and the session is flagged for a reset on the next batch chunk.

---

## 3. DOWNLOAD EXTRACTION & CORRUPTED DOWNLOADS

- **Blob Extraction Protocol**: Gemini UI does not offer a direct static download link for generated images. The script executes JS inside the browser session using `canvas.toDataURL()` to extract the raw base64 data. 
- **Sync Fallback**: If canvas extraction fails, a fallback synchronous XHR GET request is dispatched inside the browser page context to read the blob data directly.
- **Corrupted/Empty Checks**: The base64 data is split and decoded. If the payload size is < 1000 bytes, it is rejected as a blank canvas error and logged as a failure.
- **Filename Collision Prevention**: Files are saved in `render_output/raw/` as `<passport_stem>.png`. If a collision occurs, a unique timestamp suffix is appended (`_dup<timestamp>`).

---

## 4. FAILURE RECOVERY & RETRY BEHAVIOR

- **State Reconstruction**: The script implements recovery from forced session failures. If a timeout, send error, or extraction error occurs, the script:
  1. Captures a browser screenshot.
  2. Appends a failure record to the visible `/render_output/failed_logs/failures.log`.
  3. Sets `need_reset = True`, which triggers a `prime_gemini()` call at the start of the next file to reset the driver session and context.
- **Batch Chunking**: To prevent memory leaks and contextual dilution, the chat session is reset and re-initialized with the role priming prompt every `BATCH_SIZE = 5` items.
- **Raw vs Processed Synchronization**: Images are post-processed via `image_postprocessor.py`. Successful runs copy and validate from raw directly to `processed/`. Failed post-processing moves the outputs to `failed/` and logs the event without blocking the parent loop.
