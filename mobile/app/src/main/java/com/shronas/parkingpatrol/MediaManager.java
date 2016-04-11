package com.shronas.parkingpatrol;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Environment;
import android.os.Message;
import android.widget.Toast;

import java.io.File;
import java.util.ArrayList;

import dji.sdk.Camera.DJIMedia;
import dji.sdk.Camera.DJIMediaManager;
import dji.sdk.base.DJIBaseComponent;
import dji.sdk.base.DJIError;

/**
 * Created by Shronas on 3/15/16.
 * class MediaManager encapsulates media scanning processes.
 */
public class MediaManager {
    private DJIMediaManager mMediaManager = null;
    Activity mActivity;

    MediaManager(DJIMediaManager mMediaManager, Activity mActivity) {
        this.mMediaManager = mMediaManager;
        this.mActivity = mActivity;
    } // constructor MediaManager()


    protected boolean isMediaManagerAvailable() {
        return (null != mMediaManager);
    } // isMediaManagerAvailable()


    void fetchList() {
        mMediaManager.setCameraModeMediaDownload(
                new DJIBaseComponent.DJICompletionCallback() {
                    @Override
                    public void onResult(DJIError error) {
                        if (error == null) {
                            showToast("media manager set");
                        } else {
                            showToast(error.getDescription());
                        }
                    } // onResult()
                }); // callback

        mMediaManager.fetchMediaList(
                new DJIMediaManager.CameraDownloadListener<ArrayList<DJIMedia>>() {

                    @Override
                    public void onFailure(DJIError error) {
                        Message message = Message.obtain();
                        message.obj = error.toString();
                        //messageHandler.sendMessage(message);
                    } // onFailure()

                    @Override
                    public void onProgress(long total, long current) {
                        Message message = Message.obtain();
                        message.obj = "Progress: " + current + " / " + total;
                        //messageHandler.sendMessage(message);
                    } // onProgress()

                    @Override
                    public void onRateUpdate(long total, long current, long persize) {
                    } // onRateUpdate()

                    @Override
                    public void onStart() {
                        Message message = Message.obtain();
                        message.obj = "Start";
                        //messageHandler.sendMessage(message);
                    } // onStart()

                    @Override
                    public void onSuccess(ArrayList<DJIMedia> data) {
                        showToast("fetchMediaList success");
                        downloadImage(data);
                    } // onSuccess()
                }); // fetchMediaList()
    } // fetchMediaList()



    protected void downloadImage(ArrayList<DJIMedia> data) {
        int image_index = data.size() - 1;
        DJIMedia image = data.get(image_index);
        String filename = image.getFileName();

        final String test_filename = filename;

        // remove extension
        int pos = filename.lastIndexOf(".");
        if (pos > 0)
            filename = filename.substring(0, pos);

        File destDir = new File(Environment.getExternalStorageDirectory().
                getAbsolutePath() + "/DJI_SPALSH/");

        final File destDir2 = destDir;

        image.fetchMediaData(destDir, filename,
                new DJIMediaManager.CameraDownloadListener<String>() {

                    @Override
                    public void onFailure(DJIError error) {
                        Message message = Message.obtain();
                        message.obj = error.toString();
                        //messageHandler.sendMessage(message);
                    } // onFailure()

                    @Override
                    public void onProgress(long total, long current) {
                        Message message = Message.obtain();
                        //message.obj = "Progress: " + i;
                        //messageHandler.sendMessage(message);
                    } // onProgress()

                    @Override
                    public void onRateUpdate(long total, long current, long persize) {
                    } // onRateUpdate()

                    @Override
                    public void onStart() {
                        Message message = Message.obtain();
                        message.obj = "Start";
                        //messageHandler.sendMessage(message);
                    } // onStart()

                    @Override
                    public void onSuccess(String data) {
                        showToast("image download success");
                        mMediaManager.exitMediaDownloading();

                        String destDirectory = Environment.getExternalStorageDirectory().
                                getAbsolutePath() + "/DJI_SPALSH/";
                        mActivity.sendBroadcast(new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, Uri.parse("file://" + destDirectory)));

                        ((MainActivity) mActivity).postDownload(destDirectory + test_filename);
                    } // onSuccess()
                }); // fetchMediaList()
    } // downloadImage()


    public void showToast(final String msg) {
        mActivity.runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(mActivity, msg, Toast.LENGTH_SHORT).show();
            }
        });
    } // showToast()
} // class MediaManager()
