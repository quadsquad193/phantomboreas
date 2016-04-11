package com.shronas.parkingpatrol;

import java.util.ArrayList;

/**
 * Created by Shronas on 4/9/16.
 * Aggregates info to post to server
 */
public class Uploadable {
    private String filename;
    private double latitude;
    private double longitude;
    private Long timestamp;


    Uploadable(String filename, double latitude, double longitude, Long timestamp) {
        this.filename = filename;
        this.latitude = latitude;
        this.longitude = longitude;
        this.timestamp = timestamp;
    } // Uploadable()


    public String getFilename() {
        return filename;
    } // getFilenames()


    public double getLatitude() {
        return latitude;
    } // getLatitude()


    public double getLongitude() {
        return longitude;
    } // getLongitude()


    public Long getTimestamp() {
        return timestamp;
    } // getTimestamp()
} //  class Uploadable
