package com.quadsquad193.parkingpatrol;

/**
 * Created by Shronas on 11/23/15.
 * Grid Item Class to represent individual items in the grid
 */
public class GalleryItem {
    String filename;
    String dateTime;
    String loc;

    GalleryItem(String filename, String dateTime, String loc) {
        this.filename = filename;
        this.dateTime = dateTime;
        this.loc = loc;
    } // GalleryItem()
} // class GalleryItem
