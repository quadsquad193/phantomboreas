package com.shronas.parkingpatrol;

import android.app.Activity;
import android.util.Log;

import dji.sdk.Camera.DJICamera;
import dji.sdk.SDKManager.DJISDKManager;
import dji.sdk.base.DJIBaseProduct;

/**
 * Created by Shronas on 3/15/16.
 * Product class encapsulates code relating to DJI Phantom 3 Object
 */
public class Product {
    private DJIBaseProduct mProduct = null;
    private Camera mCamera = null;
    private Activity mActivity;

    Product(Activity mActivity) {
        this.mActivity = mActivity;

        try {
            updateProduct();
        } catch (Exception exception) {
            mProduct = null;
        } // try/catch
    } // constructor Product()


    DJIBaseProduct getProduct() {
        updateProduct();
        return this.mProduct;
    } // getProduct()


    void updateProduct() {
        mProduct = ParkingPatrolApplication.getProductInstance();
        if (mProduct != null)
            mCamera = new Camera(mProduct.getCamera(), mActivity);
        else
            Log.d("updateProduct", "product not connected");
    } // updateProduct()


    Camera getCamera() {
        updateProduct();
        return this.mCamera;
    } // getCamera()


    protected boolean isConnected() {
        return (null != this.getProduct()) && mProduct.isConnected();
    } // isProductModuleAvailable()


    protected void capturePhoto() {
        getCamera().capturePhoto();
    } // capturePhoto()


    protected void record() {
        getCamera().record();
    } // capturePhoto()


    protected void stopRecord() {
        getCamera().stopRecord();
    } // capturePhoto()
} // class Product
