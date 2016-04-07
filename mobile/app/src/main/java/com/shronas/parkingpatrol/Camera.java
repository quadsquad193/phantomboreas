package com.shronas.parkingpatrol;

import android.app.Activity;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;

import dji.sdk.Camera.DJICamera;
import dji.sdk.Camera.DJICameraSettingsDef;
import dji.sdk.base.DJIBaseComponent;
import dji.sdk.base.DJIError;

/**
 * Created by Shronas on 3/15/16.
 * class encapsulates Camera processes
 */
public class Camera {
    private DJICamera mCamera = null;
    private MediaManager mMediaManager;
    Activity mActivity;

    private int i = 0;
    private int TIME = 1000;

    Camera(DJICamera mCamera, Activity mActivity) {
        this.mActivity = mActivity;
        this.mCamera = mCamera;
    } // Camera()


    /**
     * Before the download commands are sent to the aircraft, the camera work mode should be set
     * to download mode.
     */
    protected void setupCamera() {
        setDownloadMode();

        if (mCamera != null)
            mMediaManager = new MediaManager(mCamera.getMediaManager(), mActivity);
        else
            Log.d("setupCamera", "camera null");

        if (mMediaManager.isMediaManagerAvailable()) {
            mMediaManager.fetchList();
        } else {
            if(mActivity == null)
                Log.d("In Download", "Media Download not available");
            else
                showToast("In Download: Media Download not available");
        }
    } // setupCamera()


    void setDownloadMode() {
        mCamera.setCameraMode(
                DJICameraSettingsDef.CameraMode.MediaDownload,
                new DJIBaseComponent.DJICompletionCallback() {
                    @Override
                    public void onResult(DJIError djiError) {}
                } // callback
        ); // setCameraMode()
    } // setDownloadMode()


    void capturePhoto() {
        DJICameraSettingsDef.CameraMode cameraMode = DJICameraSettingsDef.CameraMode.ShootPhoto;
        mCamera.setCameraMode(cameraMode, new DJIBaseComponent.DJICompletionCallback() {
            @Override
            public void onResult(DJIError error) {
                if (error == null) {
                    DJICameraSettingsDef.CameraShootPhotoMode photoMode = DJICameraSettingsDef.CameraShootPhotoMode.Single; // Set the camera capture mode as Single mode

                    mCamera.startShootPhoto(photoMode, new DJIBaseComponent.DJICompletionCallback() {
                        @Override
                        public void onResult(DJIError error) {
                            if (error == null) {
                                if(mActivity == null)
                                    Log.d("take photo", "success");
                                else
                                    showToast("take photo: success");
                                setupCamera();
                            } else {
                                if(mActivity == null)
                                    Log.d("photo shoot error", error.getDescription());
                                else
                                    showToast(error.getDescription());
                            }
                        }
                    }); // Execute the startShootPhoto API
                } else {
                    if(mActivity == null)
                        Log.d("set camera error", error.getDescription());
                    else
                        showToast(error.getDescription());
                }
            }
        });
    } // capturePhoto();


    void record() {
        DJICameraSettingsDef.CameraMode cameraMode = DJICameraSettingsDef.CameraMode.RecordVideo;

        mCamera.setCameraMode(cameraMode, new DJIBaseComponent.DJICompletionCallback() {

            @Override
            public void onResult(DJIError error) {
                if (error == null) {
                    mCamera.startRecordVideo(new DJIBaseComponent.DJICompletionCallback() {

                        @Override
                        public void onResult(DJIError error) {
                            if (error == null) {
                                if(mActivity == null)
                                    Log.d("Record Video", "success");
                                else
                                    showToast("Record video: success");
                                //handlerTimer.postDelayed(runnable, TIME); // Start the timer for recording
                            } else {
                                if(mActivity == null)
                                    Log.d("video record error", error.getDescription());
                                else
                                    showToast(error.getDescription());
                            }
                        }

                    }); // Execute the startShootPhoto API
                } else {
                    if(mActivity == null)
                        Log.d("set video record mode", error.getDescription());
                    else
                        showToast(error.getDescription());
                }
            }
        });
    } // record()


    private Handler handlerTimer = new Handler();
    Runnable runnable = new Runnable() {
        @Override
        public void run() {
            // handler自带方法实现定时器
            try {
                handlerTimer.postDelayed(this, TIME);
                //viewTimer.setText(Integer.toString(i++));
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    };

    void stopRecord() {
        mCamera.stopRecordVideo(new DJIBaseComponent.DJICompletionCallback() {

            @Override
            public void onResult(DJIError error) {
                if (error == null) {
                    if(mActivity == null)
                        Log.d("Stop recording", "success");
                    else
                        showToast("Stop recording: success");
                } else {
                    if(mActivity == null)
                        Log.d("stop recording error", error.getDescription());
                    else
                        showToast(error.getDescription());
                }
                handlerTimer.removeCallbacks(runnable); // Start the timer for recording
                // i = 0; // Reset the timer for recording
            }

        });
    } // stopRecord()


    public void showToast(final String msg) {
        if (mActivity != null) {
            mActivity.runOnUiThread(new Runnable() {
                public void run() {
                    Toast.makeText(mActivity, msg, Toast.LENGTH_SHORT).show();
                }
            });
        } // if activity isn't null
    } // showToast()
} // class Camera