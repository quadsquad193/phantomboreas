package com.quadsquad193.parkingpatrol;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.graphics.SurfaceTexture;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.TextureView;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import dji.sdk.AirLink.DJILBAirLink;
import dji.sdk.Camera.DJICamera;
import dji.sdk.Codec.DJICodecManager;
import dji.sdk.Products.DJIAircraft;
import dji.sdk.base.DJIBaseProduct;

/**
 * Created by Shronas on 5/13/16.
 * Fragment displaying stream overlay with image capture functionality
 */
public class StreamFragment extends Fragment implements TextureView.SurfaceTextureListener,View.OnClickListener  {
    public Activity mActivity;
    public Handler messageHandler;

    private static final String TAG = "Video Stream";

    private static final int INTERVAL_LOG = 300;
    private static long mLastTime = 0l;

    protected DJICamera.CameraReceivedVideoDataCallback mReceivedVideoDataCallBack = null;
    protected DJILBAirLink.DJIOnReceivedVideoCallback mOnReceivedVideoCallback = null;

    Product mProductEncapsulated;

    // Codec for video live view
    protected DJICodecManager mCodecManager = null;

    protected TextView mConnectStatusTextView;
    //Video Preview
    protected TextureView mVideoSurface = null;
    private ImageButton captureAction, recordAction, captureMode;
    private TextView viewTimer;

    public StreamFragment() {}

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        mActivity = getActivity();
        return inflater.inflate(R.layout.fragment_stream, container, false);
    } // onCreateView()


    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        super.onActivityCreated(savedInstanceState);

        initUI();

        Looper looper = Looper.myLooper();
        messageHandler = new MessageHandler(looper);

        // The callback for receiving the raw H264 video data for camera live view
        mReceivedVideoDataCallBack = new DJICamera.CameraReceivedVideoDataCallback() {

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
        mOnReceivedVideoCallback = new DJILBAirLink.DJIOnReceivedVideoCallback() {

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
        mActivity.registerReceiver(mReceiver, filter);

        mProductEncapsulated = new Product(this, mActivity);

        SharedPreferences prefs = mActivity.getSharedPreferences(
                TabActivity.PACKAGE_NAME, Context.MODE_PRIVATE);

        getTokenAsync getTokenTask = new getTokenAsync(mActivity);
        // if token doesn't already exist or it is empty
        //if (!prefs.contains("token") || prefs.getString("token", "").isEmpty())
        getTokenTask.execute(); // get token every time the app starts
    } // onActivityCreated()


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


    @Override
    public void onDestroy() {
        Log.e(TAG, "onDestroy");
        uninitPreviewer();
        mActivity.unregisterReceiver(mReceiver);
        super.onDestroy();
    }


    private void initUI() {
        mConnectStatusTextView = (TextView) mActivity.findViewById(R.id.ConnectStatusTextView);
        mVideoSurface = (TextureView) mActivity.findViewById(R.id.video_previewer_surface);
        captureAction = (ImageButton) mActivity.findViewById(R.id.button1);

        if (null != mVideoSurface)
            mVideoSurface.setSurfaceTextureListener(this);

        captureAction.setOnClickListener(this);
    } // initUI()


    private void initPreviewer() {
        DJIBaseProduct mProduct = mProductEncapsulated.getProduct();
        DJICamera mCamera = null;
        if (mProduct != null)
            mCamera = mProduct.getCamera();
        //else
        //  showToast(getString(R.string.disconnected));

/*
        if () {
            showToast(getString(R.string.disconnected));
        }*/

        if ((null != mProduct) && mProduct.isConnected()) {
            if (null != mVideoSurface) {
                mVideoSurface.setSurfaceTextureListener(this);
            }

            if (!mProduct.getModel().equals(DJIBaseProduct.Model.UnknownAircraft)) {
                //mCamera = mProductEncapsulated.getCamera();
                if (mCamera != null) {
                    // Set the callback
                    mCamera.setDJICameraReceivedVideoDataCallback(mReceivedVideoDataCallBack);
                    //mPlaybackManager = mCamera.getPlayback();
                }
                //else
                //  showToast(getString(R.string.camera_disconnected));
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
        DJIBaseProduct mProduct = mProductEncapsulated.getProduct();
        DJICamera mCamera;

        /*if (null == mProduct || !mProduct.isConnected()) {
            showToast(getString(R.string.disconnected));
        } else {*/
        if ((null != mProduct) && mProduct.isConnected()) {
            if (!mProduct.getModel().equals(DJIBaseProduct.Model.UnknownAircraft)) {
                mCamera = mProduct.getCamera();
                if (mCamera != null) {
                    // Set the callback
                    mCamera.setDJICameraReceivedVideoDataCallback(null);
                }
                //else
                //  showToast(getString(R.string.camera_disconnected));
            } else {
                if (null != mProduct.getAirLink()) {
                    if (null != mProduct.getAirLink().getLBAirLink()) {
                        // Set the callback
                        mProduct.getAirLink().getLBAirLink().setDJIOnReceivedVideoCallback(null);
                    }
                }
            }
        }
        //else
        //  showToast(getString(R.string.disconnected));
    }


    //
    @Override
    public void onSurfaceTextureAvailable(SurfaceTexture surface,int width, int height) {
        Log.e(TAG, "onSurfaceTextureAvailable");
        if (mCodecManager == null) {
            Log.e(TAG, "mCodecManager is null 2");
            mCodecManager = new DJICodecManager(mActivity, surface, width, height);
        }
    }


    //
    @Override
    public void onSurfaceTextureSizeChanged(SurfaceTexture surface,int width, int height){
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


    public void showToast(final String msg) {
        mActivity.runOnUiThread(new Runnable() {
            public void run() {
                Toast.makeText(mActivity, msg, Toast.LENGTH_SHORT).show();
            }
        });
    }


    protected void onProductChange() {
        initPreviewer();
    }


/*
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
        return mActivity.super.dispatchTouchEvent(ev);
    }
*/


    @Override
    public void onClick(View v) {
        if (!mProductEncapsulated.isConnected()) {
            showToast(getString(R.string.disconnected));
            return;
        }

        switch (v.getId()) {
            case R.id.button1: {
                mProductEncapsulated.capturePhoto();
                break;
            }
            default:
                break;
        }
    }


    public void postDownload(String path) {
        final String filePath = path;
        final Fragment mFragment = this;

        mActivity.runOnUiThread(new Runnable() {
            public void run() {
                if (filePath.isEmpty()) {
                    showToast("Unable to retrieve image capture");
                    return;
                }

                //showToast(filePath);
                uploadAsync server = new uploadAsync(mActivity);

                double latitude = mProductEncapsulated.getLatitude();
                double longitude = mProductEncapsulated.getLongitude();

                if (Double.isNaN(latitude))
                    latitude = 0;
                if (Double.isNaN(longitude))
                    longitude = 0;

                Long timestamp = System.currentTimeMillis() / 1000; // need in seconds
                Uploadable uploadable = new Uploadable(filePath, latitude, longitude, timestamp);

                server.execute(uploadable);
            }
        });
    } // postDownload()


    class MessageHandler extends Handler {
        public MessageHandler(Looper looper) {
            super(looper);
        }

        public void handleMessage(Message msg) {
            //mTexInfo.setText((String)msg.obj);
        }
    }
} // StreamFragment