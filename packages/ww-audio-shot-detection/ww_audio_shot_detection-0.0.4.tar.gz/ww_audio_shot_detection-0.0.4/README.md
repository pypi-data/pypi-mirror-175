# BallTracking Annotator
### Required Software
- Python3.6.9
- virtualenv

### Installation
```sh
export PYTHON3_PATH=PATH_TO_YOUR_PYTHON3_BIN_HERE
./install
```
### To Run [Command Line]
There are several steps within the pipeline each with their own bash script wrapper
1. The first step is done with a playstation 4 controller.  The user then does their best to keep the bouning box around the wall for the entirety of the video.  There are also commands to rewind, pause, speed up, and slow down.
    To start this step:
    ```sh
    ./big_box_track VIDEO_PATH_HERE
    ```
    As long as no other future steps have been run this step can be rerun to make fixes, etc..
2. This requires no user interaction.  This step finds the smaller bounding box within the bounding boxes the user made in step 1.
    ```sh
    ./auto_track VIDEO_PATH_HERE
    ```
3. This is used to find any poorly placed tight bounding boxes and fix them.  Also done with a PS4 controller.
    ```sh
    ./edit_auto_det VIDEO_PATH_HERE
    ```
4. This goes to any frame where no ball could be detected in the bounding box created in step 1 and allows the user to fill them in.
    ```sh
    ./edit_undet VIDEO_PATH_HERE
    ```
5. Creates the annnotation output and allows for final sanity checks.
    ```sh
    ./create_annotations VIDEO_PATH_HERE
    ```
6. Uploads the videos to S3 and saves to a DynamoDB database
    ```sh
    ./upload VIDEO_PATH_HERE
    ```

### To Run [UI (PyQt]


