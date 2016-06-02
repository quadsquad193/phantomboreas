package com.quadsquad193.parkingpatrol;

import android.os.Environment;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.v7.widget.GridLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.io.File;
import java.util.ArrayList;

/**
 * A placeholder fragment containing a simple view.
 */
public class DJIGalleryFragment extends Fragment {
    private RecyclerView mRecyclerView;
    private RecyclerView.Adapter mAdapter;
    private RecyclerView.LayoutManager mLayoutManager;

    private final String TAG = "DJIGalleryFragment";

    public DJIGalleryFragment() {}

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        View root = inflater.inflate(R.layout.fragment_gallery, container, false);

        mRecyclerView = (RecyclerView) root.findViewById(R.id.gallery_view);

        // use this setting to improve performance if you know that changes
        // in content do not change the layout size of the RecyclerView
        mRecyclerView.setHasFixedSize(true);

        // use a linear layout manager
        mLayoutManager = new GridLayoutManager(this.getActivity(), 2);
        mRecyclerView.setLayoutManager(mLayoutManager);

        ArrayList<GalleryItem> gridList = getListItems();

        mAdapter = new GalleryGridAdapter(gridList, getActivity());
        mRecyclerView.setAdapter(mAdapter);

        return root;
    }



    ArrayList<GalleryItem> getListItems() {
        String path = Environment.getExternalStorageDirectory().getAbsolutePath()
                + getActivity().getString(R.string.capture_dir);
        Log.d(TAG, "Path: " + path);

        File dir = new File(path);
        File files[] = dir.listFiles();
        ArrayList<GalleryItem> itemArrayList = new ArrayList<>();

        if (files == null)
            return null;

        Log.d(TAG, "Size: "+ files.length);

        for (File file : files) {
            String fullPathName = path + file.getName();

            String filenameArray[] = file.getName().split("\\.");
            String extension = filenameArray[filenameArray.length - 1];

            if (!extension.toLowerCase().equals("jpeg") && !extension.toLowerCase().equals("jpg"))
                continue;

            GalleryItem item = new GalleryItem(fullPathName, "Date", "Loc");
            itemArrayList.add(item);
        } // for each image

        /*for (int i=0; i < file.length; i++)
        {
            Log.d(TAG, "FileName:" + file[i].getName());
        }*/

        return itemArrayList;
    } // getListItems()
} // DJIGalleryFragment