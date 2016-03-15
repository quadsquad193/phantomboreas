package com.shronas.parkingpatrol;

import android.app.Activity;

import dji.sdk.base.DJIBaseProduct;

/**
 * Created by Shronas on 3/15/16.
 * Product class encapsulates code relating to DJI Phantom 3 Object
 */
public class Product {
    private DJIBaseProduct mProduct = null;
    private Camera mCamera;
    private Activity mActivity;

    Product(Activity mActivity) {
        try {
            mProduct = ParkingPatrolApplication.getProductInstance();
            mCamera = new Camera(mProduct.getCamera(), mActivity);
        } catch (Exception exception) {
            mProduct = null;
        } // try/catch
    } // constructor Product()


    DJIBaseProduct getProduct() {
        return this.mProduct;
    } // getProduct()


    Camera getCamera() {
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
