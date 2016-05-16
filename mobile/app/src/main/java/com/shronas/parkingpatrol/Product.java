package com.shronas.parkingpatrol;

import android.app.Activity;
import android.os.Environment;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;

import dji.sdk.Camera.DJICamera;
import dji.sdk.FlightController.DJIFlightController;
import dji.sdk.Products.DJIAircraft;
import dji.sdk.SDKManager.DJISDKManager;
import dji.sdk.base.DJIBaseProduct;

/**
 * Created by Shronas on 3/15/16.
 * Product class encapsulates code relating to DJI Phantom 3 Object
 */
public class Product {
    private DJIBaseProduct mProduct = null;
    private Camera mCamera = null;
    private Fragment returnFragment;
    private Activity mActivity;

    Product(Fragment returnFragment, Activity mActivity) {
        this.mActivity = mActivity;
        this.returnFragment = returnFragment;

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


    Camera getCamera() {
        updateProduct();
        return this.mCamera;
    } // getCamera()


    void updateProduct() {
        mProduct = ParkingPatrolApplication.getProductInstance();
        if (mProduct != null)
            mCamera = new Camera(mProduct.getCamera(), returnFragment, mActivity);
        else
            Log.d("updateProduct", "product not connected");
    } // updateProduct()


    double getLatitude() {
        if (mProduct == null)
            return 0;

        DJIFlightController mFlightController = ((DJIAircraft) mProduct).getFlightController();
        return mFlightController.getCurrentState().getAircraftLocation().getLatitude();
    } // getLatitude


    double getLongitude() {
        if (mProduct == null)
            return 0;

        DJIFlightController mFlightController = ((DJIAircraft) mProduct).getFlightController();
        return mFlightController.getCurrentState().getAircraftLocation().getLongitude();
    } // getLongitude


    protected boolean isConnected() {
        return (null != this.getProduct()) && mProduct.isConnected();
    } // isProductModuleAvailable()


    protected void capturePhoto() {
        if (null != mCamera)
            getCamera().capturePhoto();
    } // capturePhoto()


   /* protected void record() {
        getCamera().record();
    } // capturePhoto()


    protected void stopRecord() {
        getCamera().stopRecord();
    } // capturePhoto()*/
} // class Product
