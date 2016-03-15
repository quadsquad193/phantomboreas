package com.shronas.parkingpatrol;

import android.content.Context;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by Shronas on 2/23/16.
 * Handles Uploading of images to a server
 * Params used:
 * Longitude of Quadcopter location upon image capture
 * Latitude of Quadcopter location upon image capture
 * Timestamp of when image was captured
 */

public class UploadAsyncTask extends AsyncTask<String, Void, Void> {
    private final String LOG_TAG = UploadAsyncTask.class.getSimpleName();
    private Context context;

    String lineEnd = "\r\n";
    String twoHyphens = "--";
    String boundary = "fae6ba7e-ab3b-4696-90de-d52de8f11947";
    HttpURLConnection urlConnection = null;
    DataOutputStream dos = null;
    final String TAG = "UploadAsyncTask";

    public UploadAsyncTask(Context context) {
        this.context = context;
    } // UploadAsyncTask()


    protected void onPreExecute() {
        Toast.makeText(context, "Uploading image ...", Toast.LENGTH_SHORT).show();
    } // onPreExecute()


    @Override
    protected Void doInBackground(String... filenames) {
        String param_name[] = { "latitude", "longitude", "timestamp" };
        String param_value[] = { "31.179910", "-98.173828", "1457138772" };

        File image;
        int num = filenames.length;

        Log.d(TAG, Integer.toString(num));

        try {
            for (String filepath : filenames) {
                image = new File(filepath);
                Log.d(TAG, "image found at: "+ filepath);

                setupConnection(filepath);

                /* Adding params & image */
                for (int index = 0; index < param_name.length; index++)
                    writeParam(param_name[index], param_value[index]);
                writeImage(image, filepath);

                Log.d(TAG, "Server response" + handleResponse());

                closeConnection();
            } // for each image
        } catch(FileNotFoundException e) {
            e.printStackTrace();
            Log.d(TAG, "can't find image");
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (urlConnection != null)
                urlConnection.disconnect();
        } // end try/catch/finally block

        return null;
    } // doInBackground()


    /* Setup HTTPUrlConnection */
    private void setupConnection(String filepath) throws IOException {
        //URL url = new URL("http://taglab3.genomecenter.ucdavis.edu/hri/api/active/");
        URL url = new URL("http://10.42.0.1:8000/droneimages");
        //URL url = new URL("http://requestb.in/12482fb1");
        urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setDoInput(true); // Allow Inputs
        urlConnection.setDoOutput(true); // Allow Outputs
        urlConnection.setUseCaches(false); // Don't use a Cached Copy
        urlConnection.setRequestMethod("POST");
        urlConnection.setRequestProperty("Connection", "Keep-Alive");
        //urlConnection.setChunkedStreamingMode(0); // don't buffer to preserver heap space.

        urlConnection.setRequestProperty("Content-Type", "multipart/form-data;boundary=" + boundary);
        urlConnection.setRequestProperty("image", filepath);
        urlConnection.setRequestProperty("Content-Language", "en-US");
        urlConnection.connect();

        dos = new DataOutputStream(urlConnection.getOutputStream());
    } // setupConnection


    /* Close streams and URL connection */
    private void closeConnection() throws IOException {
        dos.flush();
        dos.close();
        urlConnection.disconnect();
    } // closeConnection()


    /* Function writes a text param to a given stream */
    private void writeParam(String param_name, String param_value) throws IOException {
        dos.writeBytes(twoHyphens + boundary + lineEnd);
        dos.writeBytes("Content-Disposition: form-data; name=\"" + param_name + "\"" + lineEnd);
        dos.writeBytes("Content-Type: text/plain; charset=UTF-8" + lineEnd);
        dos.writeBytes("Content-Transfer-Encoding: 8bit" + lineEnd);
        dos.writeBytes("Content-Length: " + param_value.length() + lineEnd);
        dos.writeBytes(lineEnd);
        dos.writeBytes(param_value);
        dos.writeBytes(lineEnd);
    } // writeParam


    /* Function writes an image binary to a given stream */
    private void writeImage(File image, String filepath) throws IOException {
        int bytesRead, bytesAvailable, bufferSize;
        byte[] buffer;
        int maxBufferSize = 1024 * 1024;
        FileInputStream fileInputStream;

        try {
            fileInputStream = new FileInputStream(image);
            // create a buffer of maximum size
            bytesAvailable = fileInputStream.available();

            dos.writeBytes(twoHyphens + boundary + lineEnd);
            dos.writeBytes("Content-Disposition: form-data; name=\"image\";filename=\""+ filepath + "\"" + lineEnd);
            dos.writeBytes("Content-Type: image/jpeg" + lineEnd);
            dos.writeBytes("Content-Transfer-Encoding: binary" + lineEnd);
            dos.writeBytes("Content-Length: " + bytesAvailable + lineEnd);
            dos.writeBytes(lineEnd);

            bufferSize = Math.min(bytesAvailable, maxBufferSize);
            buffer = new byte[bufferSize];
            // read file and write it into form...
            bytesRead = fileInputStream.read(buffer, 0, bufferSize);

            while (bytesRead > 0) {
                Log.d("Sending", Integer.toString(bufferSize) + " bytes");

                dos.write(buffer, 0, bufferSize);
                bytesAvailable = fileInputStream.available();
                bufferSize = Math.min(bytesAvailable, maxBufferSize);
                bytesRead = fileInputStream.read(buffer, 0, bufferSize);
            } // while there are bytes left to send ...

            dos.writeBytes(lineEnd);
            dos.writeBytes(twoHyphens + boundary + twoHyphens + lineEnd);
            fileInputStream.close();
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
    } // writeImage()


    /* Handles URL Connection Response */
    private String handleResponse() throws IOException {
        int serverResponseCode = urlConnection.getResponseCode();
        String serverResponseMessage = urlConnection.getResponseMessage();

        Log.i(TAG, "File upload response" + "HTTP Response is : " + serverResponseMessage + ": " + serverResponseCode);

        if (serverResponseCode == 200)
            Log.d(TAG, "Upload result" + "Success! =)");

        /* Server response message */
        InputStream is = urlConnection.getInputStream();
        BufferedReader rd = new BufferedReader(new InputStreamReader(is));
        String line;
        StringBuilder response = new StringBuilder();

        while((line = rd.readLine()) != null) {
            response.append(line);
            response.append('\r');
        } // while: read each line

        rd.close();

        return response.toString();
    } // handleResponse()
} // class UploadAsyncTask