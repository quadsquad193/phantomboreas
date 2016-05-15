package com.shronas.parkingpatrol;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.media.ExifInterface;
import android.media.Image;
import android.media.ThumbnailUtils;
import android.net.Uri;
import android.os.AsyncTask;
import android.support.v4.graphics.BitmapCompat;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;

import com.squareup.picasso.Picasso;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.List;

/**
 * Created by Shronas on 11/23/15.
 * Grid Adapter for Gallery
 */

public class GalleryGridAdapter extends RecyclerView.Adapter<GalleryGridAdapter.ViewHolder> {
    private List<GalleryItem> mDataset;
    private Context context;
    private final String TAG = "GalleryGridAdapter";

    ViewHolder holder;
    int position;


    // Provide a reference to the views for each data item
    // Complex data items may need more than one view per item, and
    // you provide access to all the views for a data item in a view holder
    public static class ViewHolder extends RecyclerView.ViewHolder {
        // each data item is just a string in this case
        public View mItemView;
        public ViewHolder(View v) {
            super(v);
            mItemView = v;
        }
    }


    // Provide a suitable constructor (depends on the kind of dataset)
    public GalleryGridAdapter(List<GalleryItem> myDataset, Context context) {
        mDataset = myDataset;
        this.context = context;
    }


    // Create new views (invoked by the layout manager)
    @Override
    public GalleryGridAdapter.ViewHolder onCreateViewHolder(ViewGroup parent,
                                                   int viewType) {
        // create a new view
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.gallery_image, parent, false);

        ViewGroup.LayoutParams layoutParams = v.getLayoutParams();
        layoutParams.height = layoutParams.width;
        v.setLayoutParams(layoutParams);

        // set the view's size, margins, paddings and layout parameters
        ViewHolder vh = new ViewHolder(v);

        return vh;
    }


    // Replace the contents of a view (invoked by the layout manager)
    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
        this.holder = holder;
        this.position = position;

        // - get element from your dataset at this position
        // - replace the contents of the view with that element
        ImageView mImage = (ImageView) holder.mItemView.findViewById(R.id.image);
        TextView mDate = (TextView) holder.mItemView.findViewById(R.id.date);
        TextView mTime = (TextView) holder.mItemView.findViewById(R.id.time);

        File file = new  File(mDataset.get(position).filename);

        Picasso.with(context)
                .load(file)
                .resize(512, 512)
                .centerCrop()
                .placeholder(R.drawable.white)
                .into(mImage);

        ExifInterface intf = null;
        String dateString, dateFormat = "", timeFormat = "";
        SimpleDateFormat simpleDateFormat, convertDate, convertTime;

        try {
            intf = new ExifInterface(mDataset.get(position).filename);
        } catch(IOException e) {
            e.printStackTrace();
        } // try/catch: get image Date & Time

        if(intf != null) {
            dateString = intf.getAttribute(ExifInterface.TAG_DATETIME);

            simpleDateFormat = new SimpleDateFormat("yyyy:mm:dd hh:mm:ss");
            convertDate = new SimpleDateFormat("MMM dd, yyyy");
            convertTime = new SimpleDateFormat("h:mm aa");

            Date d = null, d2 = null;

            try {
                d = simpleDateFormat.parse(dateString);
                d2 = simpleDateFormat.parse(dateString);
            } catch (ParseException e) {
                e.printStackTrace();
            } // try/catch: parse date/time
            dateFormat = convertDate.format(d);
            timeFormat = convertTime.format(d2);
        } // if the image's "exif" date is readable

        mDate.setText(dateFormat);
        mTime.setText(timeFormat);
    } // onBindViewHolder()


    // Return the size of your dataset (invoked by the layout manager)
    @Override
    public int getItemCount() {
        return mDataset.size();
    }
}