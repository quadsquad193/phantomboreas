package com.shronas.parkingpatrol;

import android.app.Activity;
import android.os.Handler;
import android.support.v4.app.Fragment;
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
    Fragment returnFragment;
    Activity mActivity;

/*    private int i = 0;
    private int TIME = 1000;*/

    Camera(DJICamera mCamera, Fragment returnFragment, Activity mActivity) {
        this.mActivity = mActivity;
        this.returnFragment = returnFragment;
        this.mCamera = mCamera;
    } // Camera()


    void setDownloadMode() {
        if (null != mCamera) {
            mCamera.setCameraMode(
                    DJICameraSettingsDef.CameraMode.MediaDownload,
                    new DJIBaseComponent.DJICompletionCallback() {
                        @Override
                        public void onResult(DJIError djiError) {
                        }
                    } // callback
            ); // setCameraMode()
        }
    } // setDownloadMode()


    void capturePhoto() {
        if (null != mCamera) {
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
                                    if (mActivity == null)
                                        Log.d("take photo", "success");
                                    else
                                        showToast("take photo: success");
                                    downloadImage();
                                } else {
                                    if (mActivity == null)
                                        Log.d("photo shoot error", error.getDescription());
                                    else
                                        showToast(error.getDescription());
                                }
                            }
                        }); // Execute the startShootPhoto API
                    } else {
                        if (mActivity == null)
                            Log.d("set camera error", error.getDescription());
                        else
                            showToast(error.getDescription());
                    }
                }
            });
        }
    } // capturePhoto();


    /**
     * Before the download commands are sent to the aircraft, the camera work mode should be set
     * to download mode.
     */
    protected void downloadImage() {
        setDownloadMode();

        if (mCamera != null)
            mMediaManager = new MediaManager(mCamera.getMediaManager(), returnFragment, mActivity);
        else
            Log.d("downloadImage", "camera null");

        if (mMediaManager.isMediaManagerAvailable()) {
            mMediaManager.fetchList(); // trigger media manager to download image
        } else {
            if(mActivity == null)
                Log.d("In Download", "Media Download not available");
            else
                showToast("In Download: Media Download not available");
        }
    } // downloadImage()



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