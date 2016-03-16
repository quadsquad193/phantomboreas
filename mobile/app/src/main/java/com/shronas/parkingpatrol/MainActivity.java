package com.shronas.parkingpatrol;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.graphics.SurfaceTexture;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.provider.MediaStore;
import android.util.Log;
import android.view.MotionEvent;
import android.view.TextureView;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.TextureView.SurfaceTextureListener;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.util.ArrayList;

import dji.sdk.AirLink.DJILBAirLink.DJIOnReceivedVideoCallback;
import dji.sdk.Camera.DJICamera;
import dji.sdk.Camera.DJICamera.CameraReceivedVideoDataCallback;
import dji.sdk.Camera.DJIMedia;
import dji.sdk.Camera.DJIMediaManager;
import dji.sdk.Codec.DJICodecManager;
import dji.sdk.Products.DJIAircraft;
import dji.sdk.base.DJIBaseComponent;
import dji.sdk.base.DJIBaseComponent.DJICompletionCallback;
import dji.sdk.base.DJIBaseProduct;
import dji.sdk.base.DJIBaseProduct.Model;
import dji.sdk.base.DJIError;
import dji.sdk.Camera.DJICameraSettingsDef.CameraMode;
import dji.sdk.Camera.DJICameraSettingsDef.CameraShootPhotoMode;

public class MainActivity extends Activity implements SurfaceTextureListener,OnClickListener {
    private DJIMediaManager mMediaManager;
    public Handler messageHandler;

    private static final String TAG = MainActivity.class.getName();

    private static final int INTERVAL_LOG = 300;
    private static long mLastTime = 0l;

    protected CameraReceivedVideoDataCallback mReceivedVideoDataCallBack = null;
    protected DJIOnReceivedVideoCallback mOnReceivedVideoCallback = null;

    private DJIBaseProduct mProduct = null;
    private DJICamera mCamera = null;
    // Codec for video live view
    protected DJICodecManager mCodecManager = null;

    protected TextView mConnectStatusTextView;
    //Video Preview
    protected TextureView mVideoSurface = null;
    private Button captureAction, recordAction, captureMode;
    private TextView viewTimer;
    private int i = 0;
    private int TIME = 1000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        initUI();

        Looper looper = Looper.myLooper();
        messageHandler = new MessageHandler(looper);

        // The callback for receiving the raw H264 video data for camera live view
        mReceivedVideoDataCallBack = new CameraReceivedVideoDataCallback() {

            @Override
            public void onResult(byte[] videoBuffer, int size) {
                if (mCodecManager != null) {
                    // Send the raw H264 video data to codec manager for decoding
                    mCodecManager.sendDataToDecoder(videoBuffer, size);
                } else {
                    Log.e(TAG, "mCodecManager is null");
                }
            }
        };

        // The callback for receiving the raw video data from Airlink
        mOnReceivedVideoCallback = new DJIOnReceivedVideoCallback() {

            @Override
            public void onResult(byte[] videoBuffer, int size) {
                if (mCodecManager != null) {
                    // Send the raw H264 video data to codec manager for decoding
                    mCodecManager.sendDataToDecoder(videoBuffer, size);
                }
            }
        };

        // Register the broadcast receiver for receiving the device connection's changes.
        IntentFilter filter = new IntentFilter();
        filter.addAction(ParkingPatrolApplication.FLAG_CONNECTION_CHANGE);
        registerReceiver(mReceiver, filter);

/*
        String destDirectory = Environment.getExternalStorageDirectory().
                getAbsolutePath() + "/DJI_SPALSH/";
        postDownload(destDirectory + "DJI_0052.jpg");
*/

/*        if (shouldAskPermission()) {
            if (ContextCompat.checkSelfPermission(this,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE)
                    != PackageManager.PERMISSION_GRANTED) {
                if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                        Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                    // Show an expanation to the user *asynchronously* -- don't block
                    // this thread waiting for the user's response! After the user
                    // sees the explanation, try again to request the permission.
                } // if we should show reasoning for permission

                String[] perms = {"android.permission.WRITE_EXTERNAL_STORAGE"};
                this.requestPermissions(perms, PERMISSIONS_REQUEST_WRITE_EXTERNAL);
            } // if permission isn't already granted, then ask to grant it

            else {
                initPhotoPicker();
            } // else: proceed with upload
        } // shouldAskPermission()

        else
            initPhotoPicker();*/
        //setupCamera();
    }


    @Override
    public void onResume() {
        Log.e(TAG, "onResume");
        super.onResume();
        initPreviewer();
        updateTitleBar();
        if (mVideoSurface == null) {
            Log.e(TAG, "mVideoSurface is null");
        }
    }

    @Override
    public void onPause() {
        Log.e(TAG, "onPause");
        uninitPreviewer();
        super.onPause();
    }

    @Override
    public void onStop() {
        Log.e(TAG, "onStop");
        super.onStop();
    }

    public void onReturn(View view) {
        Log.e(TAG, "onReturn");
        this.finish();
    }

    @Override
    protected void onDestroy() {
        Log.e(TAG, "onDestroy");
        uninitPreviewer();

        unregisterReceiver(mReceiver);

        super.onDestroy();
    }

    private void initUI() {
        mConnectStatusTextView = (TextView) findViewById(R.id.ConnectStatusTextView);
        // init mVideoSurface
        mVideoSurface = (TextureView) findViewById(R.id.video_previewer_surface);

        viewTimer = (TextView) findViewById(R.id.timer);
        captureAction = (Button) findViewById(R.id.button1);
        recordAction = (Button) findViewById(R.id.button2);
        captureMode = (Button) findViewById(R.id.button3);

        if (null != mVideoSurface) {
            mVideoSurface.setSurfaceTextureListener(this);
        }
        captureAction.setOnClickListener(this);
        recordAction.setOnClickListener(this);
        captureMode.setOnClickListener(this);

    }

    private Handler handlerTimer = new Handler();
    Runnable runnable = new Runnable() {
        @Override
        public void run() {
            // handler自带方法实现定时器
            try {

                handlerTimer.postDelayed(this, TIME);
                viewTimer.setText(Integer.toString(i++));

            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    };

    private void initPreviewer() {
        try {
            mProduct = ParkingPatrolApplication.getProductInstance();
        } catch (Exception exception) {
            mProduct = null;
        }

        if (null == mProduct || !mProduct.isConnected()) {
            mCamera = null;
            showToast(getString(R.string.disconnected));
        }

        else {
            if (null != mVideoSurface) {
                mVideoSurface.setSurfaceTextureListener(this);
            }

            if (!mProduct.getModel().equals(Model.UnknownAircraft)) {
                mCamera = mProduct.getCamera();
                if (mCamera != null) {
                    // Set the callback
                    mCamera.setDJICameraReceivedVideoDataCallback(mReceivedVideoDataCallBack);
                    //mPlaybackManager = mCamera.getPlayback();
                }
            }

            else {
                if (null != mProduct.getAirLink()) {
                    if (null != mProduct.getAirLink().getLBAirLink()) {
                        // Set the callback
                        mProduct.getAirLink().getLBAirLink().setDJIOnReceivedVideoCallback(mOnReceivedVideoCallback);
                    }
                }
            }
        }
    }

    private void uninitPreviewer() {
        try {
            mProduct = ParkingPatrolApplication.getProductInstance();
        } catch (Exception exception) {
            mProduct = null;
        }

        if (null == mProduct || !mProduct.isConnected()) {
            mCamera = null;
            showToast(getString(R.string.disconnected));
        } else {
            if (!mProduct.getModel().equals(Model.UnknownAircraft)) {
                mCamera = mProduct.getCamera();
                if (mCamera != null) {
                    // Set the callback
                    mCamera.setDJICameraReceivedVideoDataCallback(null);
                }
            } else {
                if (null != mProduct.getAirLink()) {
                    if (null != mProduct.getAirLink().getLBAirLink()) {
                        // Set the callback
                        mProduct.getAirLink().getLBAirLink().setDJIOnReceivedVideoCallback(null);
                    }
                }
            }
        }
    }

    //
    @Override
    public void onSurfaceTextureAvailable(SurfaceTexture surface, int width, int height) {
        Log.e(TAG, "onSurfaceTextureAvailable");
        if (mCodecManager == null) {
            Log.e(TAG, "mCodecManager is null 2");
            mCodecManager = new DJICodecManager(this, surface, width, height);
        }
    }

    //
    @Override
    public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {
        Log.e(TAG, "onSurfaceTextureSizeChanged");
    }

    //
    @Override
    public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
        Log.e(TAG, "onSurfaceTextureDestroyed");
        if (mCodecManager != null) {
            mCodecManager.cleanSurface();
            mCodecManager = null;
        }

        return false;
    }

    //
    @Override
    public void onSurfaceTextureUpdated(SurfaceTexture surface) {
        Log.e(TAG, "onSurfaceTextureUpdated");
    }

    protected BroadcastReceiver mReceiver = new BroadcastReceiver() {

        @Override
        public void onReceive(Context context, Intent intent) {
            updateTitleBar();
            onProductChange();
        }

    };


    private void updateTitleBar() {
        if (mConnectStatusTextView == null) return;
        boolean ret = false;
        DJIBaseProduct product = ParkingPatrolApplication.getProductInstance();
        if (product != null) {

            if (product.isConnected()) {
                //The product is connected
                mConnectStatusTextView.setText(ParkingPatrolApplication.getProductInstance().getModel() + " Connected");
                ret = true;
            } else {

                if (product instanceof DJIAircraft) {
                    DJIAircraft aircraft = (DJIAircraft) product;
                    if (aircraft.getRemoteController() != null && aircraft.getRemoteController().isConnected()) {
                        // The product is not connected, but the remote controller is connected
                        mConnectStatusTextView.setText("only RC Connected");
                        ret = true;
                    }
                }
            }
        }

        if (!ret) {
            // The product or the remote controller are not connected.
            mConnectStatusTextView.setText("Disconnected");
        }
    }

    protected void onProductChange() {
        initPreviewer();

    }

    @Override
    public boolean dispatchTouchEvent(MotionEvent ev) {
        if (ev.getAction() == MotionEvent.ACTION_DOWN) {
            final long current = System.currentTimeMillis();
            if (current - mLastTime < INTERVAL_LOG) {
                Log.d("", "click double");
                mLastTime = 0;
            } else {
                mLastTime = current;
                Log.d("", "click single");
            }
        }
        return super.dispatchTouchEvent(ev);
    }

    public void showToast(final String msg) {
        runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show();
            }
        });
    }


    @Override
    public void onClick(View v) {

        try {
            mProduct = ParkingPatrolApplication.getProductInstance();
        } catch (Exception exception) {
            mProduct = null;
        }

        if (null == mProduct || !mProduct.isConnected()) {
            mCamera = null;
            showToast(getString(R.string.disconnected));
            return;
        }

        switch (v.getId()) {
            case R.id.button1: {
                captureAction();
                break;
            }
            case R.id.button2: {
                recordAction();
                break;
            }
            case R.id.button3: {
                stopRecord();
                break;
            }
            default:
                break;
        }
    }

    // function for taking photo
    private void captureAction() {

        CameraMode cameraMode = CameraMode.ShootPhoto;

        mCamera = mProduct.getCamera();

        mCamera.setCameraMode(cameraMode, new DJICompletionCallback() {

            @Override
            public void onResult(DJIError error) {

                if (error == null) {
                    CameraShootPhotoMode photoMode = CameraShootPhotoMode.Single; // Set the camera capture mode as Single mode

                    mCamera.startShootPhoto(photoMode, new DJICompletionCallback() {

                        @Override
                        public void onResult(DJIError error) {
                            if (error == null) {
                                showToast("take photo: success");
                                downloadButton();
                            } else {
                                showToast(error.getDescription());
                            }
                        }

                    }); // Execute the startShootPhoto API
                } else {
                    showToast(error.getDescription());
                }

            }

        });

    }

    protected boolean isProductModuleAvailable() {
        return (null != mProduct);
    }

    protected boolean isCameraModuleAvailable() {
        return isProductModuleAvailable() &&
                (null != mCamera);
    }

    protected boolean isMediaDownloadAvailable() {
        return isCameraModuleAvailable() &&
                (null != mCamera.getMediaManager());
    }

    /**
     * Before the playback commands are sent to the aircraft, the camera work mode should be set
     * to playback mode.
     */
    protected void setupCamera() {
        if (isCameraModuleAvailable()) {
            mCamera = mProduct.getCamera();

            mCamera.setCameraMode(
                    CameraMode.MediaDownload,
                    new DJIBaseComponent.DJICompletionCallback() {
                        @Override
                        public void onResult(DJIError djiError) {

                        }
                    }
            );
            if (isMediaDownloadAvailable()) {
                mMediaManager = mCamera.getMediaManager();

                mMediaManager.setCameraModeMediaDownload(
                        new DJIBaseComponent.DJICompletionCallback() {
                            @Override
                            public void onResult(DJIError error) {
                                if (error == null) {
                                    showToast("media manager set");
                                } else {
                                    showToast(error.getDescription());
                                }
                            }
                        });
            } else {
                showToast("Media Download not available");
            }
        } else
            showToast("Camera Not Available");
    }

    protected void downloadButton() {
        // Download Button
        setupCamera();

        if (isMediaDownloadAvailable()) {
            mMediaManager.fetchMediaList(
                    new DJIMediaManager.CameraDownloadListener<ArrayList<DJIMedia>>() {

                        @Override
                        public void onFailure(DJIError error) {
                            Message message = Message.obtain();
                            message.obj = error.toString();
                            messageHandler.sendMessage(message);
                        } // onFailure()

                        @Override
                        public void onProgress(long total, long current) {
                            Message message = Message.obtain();
                            message.obj = "Progress: " + i;
                            messageHandler.sendMessage(message);
                        } // onProgress()

                        @Override
                        public void onRateUpdate(long total, long current, long persize) {
                        } // onRateUpdate()

                        @Override
                        public void onStart() {
                            Message message = Message.obtain();
                            message.obj = "Start";
                            messageHandler.sendMessage(message);
                        } // onStart()

                        @Override
                        public void onSuccess(ArrayList<DJIMedia> data) {
                            showToast("fetchMediaList success");
                            downloadImage(data);
                        } // onSuccess()
                    }); // fetchMediaList()
        } // isMediaDownloadAvailable()
        else
            showToast("in download: no download media availability");
    }


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
                        messageHandler.sendMessage(message);
                    } // onFailure()

                    @Override
                    public void onProgress(long total, long current) {
                        Message message = Message.obtain();
                        message.obj = "Progress: " + i;
                        messageHandler.sendMessage(message);
                    } // onProgress()

                    @Override
                    public void onRateUpdate(long total, long current, long persize) {
                    } // onRateUpdate()

                    @Override
                    public void onStart() {
                        Message message = Message.obtain();
                        message.obj = "Start";
                        messageHandler.sendMessage(message);
                    } // onStart()

                    @Override
                    public void onSuccess(String data) {
                        showToast("image download success");
                        mMediaManager.exitMediaDownloading();

                        String destDirectory = Environment.getExternalStorageDirectory().
                                getAbsolutePath() + "/DJI_SPALSH/";
                        sendBroadcast(new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, Uri.parse("file://" + destDirectory)));

                        postDownload(destDirectory + test_filename);
                    } // onSuccess()
                }); // fetchMediaList()
    }



    private void postDownload(String path) {
        Activity mActivity = MainActivity.this;

        final String filePath = path;
        mActivity.runOnUiThread(new Runnable() {
            public void run () {
                showToast(filePath);
                UploadAsyncTask server = new UploadAsyncTask(MainActivity.this);
                server.execute(filePath);
            }
        });
    } // postDownload()



    // function for starting recording
    private void recordAction(){
        CameraMode cameraMode = CameraMode.RecordVideo;

        mCamera = mProduct.getCamera();

        mCamera.setCameraMode(cameraMode, new DJICompletionCallback() {

            @Override
            public void onResult(DJIError error) {

                if (error == null) {


                    mCamera.startRecordVideo(new DJICompletionCallback() {

                        @Override
                        public void onResult(DJIError error) {
                            if (error == null) {
                                showToast("Record video: success");
                                handlerTimer.postDelayed(runnable, TIME); // Start the timer for recording
                            } else {
                                showToast(error.getDescription());
                            }
                        }

                    }); // Execute the startShootPhoto API
                } else {
                    showToast(error.getDescription());
                }

            }

        });

    }

    // function for stopping recording
    private void stopRecord(){

        mCamera = mProduct.getCamera();

        mCamera.stopRecordVideo(new DJICompletionCallback() {

            @Override
            public void onResult(DJIError error) {
                if (error == null) {
                    showToast("Stop recording: success");
                } else {
                    showToast(error.getDescription());
                }
                handlerTimer.removeCallbacks(runnable); // Start the timer for recording
                i = 0; // Reset the timer for recording
            }

        });
    }


    public String getPath(Uri uri) {
        String[] projection = { MediaStore.MediaColumns.DATA };
        Cursor cursor = managedQuery(uri, projection, null, null, null);
        int column_index = cursor
                .getColumnIndexOrThrow(MediaStore.MediaColumns.DATA);
        cursor.moveToFirst();
        String imagePath = cursor.getString(column_index);

        return cursor.getString(column_index);
    } // getPath()


    /* Check if device is Android 6.0+ (request run-time permission check */
    private boolean shouldAskPermission(){
        return(Build.VERSION.SDK_INT > Build.VERSION_CODES.LOLLIPOP_MR1);
    } // shouldAskPermission()



    class MessageHandler extends Handler {
        public MessageHandler(Looper looper) {
            super(looper);
        }

        public void handleMessage(Message msg) {
            //mTexInfo.setText((String)msg.obj);
        }
    }

}
