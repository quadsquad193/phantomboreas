package com.quadsquad193.parkingpatrol;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Environment;
import android.util.Log;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * Created by Shronas on 2/23/16.
 * Gets a token from the server
 * Params:
 * String username: Used to authenticate app with server
 */

public class getTokenAsync extends AsyncTask<Void, Void, String> {
    private final String LOG_TAG = getTokenAsync.class.getSimpleName();
    private Context context;

    //String lineEnd = "\r\n";
    //String twoHyphens = "--";
    //String boundary = "fae6ba7e-ab3b-4696-90de-d52de8f11947";
    HttpURLConnection urlConnection = null;
    DataOutputStream dos = null;
    final String TAG = "getTokenAsync";
    String username = "";
    //String tokenKey = "token";


    public getTokenAsync(Context context) {
        this.context = context;
    } // getTokenAsync()


    protected void onPreExecute() {
        Toast.makeText(context, "Getting token ...", Toast.LENGTH_SHORT).show();

        File userFile = new File(Environment.getExternalStorageDirectory().
                getAbsolutePath() + context.getString(R.string.token_dir), context.getString(R.string.token_filename));

        if (userFile.exists()) {
            StringBuilder text = new StringBuilder();

            try {
                BufferedReader br = new BufferedReader(new FileReader(userFile));
                String line;

                while ((line = br.readLine()) != null) {
                    text.append(line);
                    text.append('\n');
                } // read each line

                br.close();
            } catch (IOException e) {
                Log.d(TAG, "Error reading contents of " + context.getString(R.string.token_filename));
            } // try/catch()

            username = text.toString();
        } // if username file was found

        else {
            Log.d(TAG, context.getString(R.string.token_filename) + " file not found in " + context.getString(R.string.token_dir));
        } // else: file not found
    } // onPreExecute()


    @Override
    protected String doInBackground(Void... params) {
        String token = "";

        try {
            requestToken();

            if (urlConnection != null)
                token = handleResponse();

            Log.d(TAG, "Token " + token);

            closeConnection();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (urlConnection != null)
                urlConnection.disconnect();
        } // end try/catch/finally block

        return token;
    } // doInBackground()


    /* Setup HTTPUrlConnection */
    private void requestToken() throws IOException {
        URL url = new URL(context.getString(R.string.get_token_url));
        urlConnection = (HttpURLConnection) url.openConnection();
        urlConnection.setDoInput(true); // Allow Inputs
        urlConnection.setDoOutput(true); // Allow Outputs
        urlConnection.setUseCaches(false); // Don't use a Cached Copy
        urlConnection.setRequestMethod("POST");
        urlConnection.setRequestProperty("Connection", "Keep-Alive");
        urlConnection.setRequestProperty("Content-Language", "en-US");
        urlConnection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");

        String content =  "authorization=" + username;
        urlConnection.setRequestProperty("Content-Length", Integer.toString(content.getBytes().length));
        urlConnection.connect();
        dos = new DataOutputStream(urlConnection.getOutputStream());
        dos.write(content.getBytes());
    } // setupConnection


    /* Close streams and URL connection */
    private void closeConnection() throws IOException {
        if (null != dos) {
            dos.flush();
            dos.close();
        }
        if (null != urlConnection)
            urlConnection.disconnect();
    } // closeConnection()


    /* Handles URL Connection Response */
    private String handleResponse() throws IOException {
        int serverResponseCode = urlConnection.getResponseCode();
        String serverResponseMessage = urlConnection.getResponseMessage();

        Log.i(TAG, "HTTP Response is : " + serverResponseMessage + ": " + serverResponseCode);

        // StringBuilder response = new StringBuilder();
        String token = "";

        if (serverResponseCode >= 200 && serverResponseCode < 300) {
            Log.d(TAG, "Server Response Success!");

            /* Server response message */
/*            InputStream is = urlConnection.getInputStream();
            BufferedReader rd = new BufferedReader(new InputStreamReader(is));
            String line;

            while ((line = rd.readLine()) != null) {
                response.append(line);
                response.append('\r');
            } // while: read each line

            rd.close();*/

            String token_unparsed = urlConnection.getHeaderField("set-cookie");

            if ( (token_unparsed != null) && !token_unparsed.isEmpty()) {
                String cookie_name_value_pair = token_unparsed.split(";")[0];
                token = cookie_name_value_pair.trim();
                Log.d(TAG, token);
            }

            if (token.isEmpty())
                Log.d(TAG, "empty token: auth failure");
        } // if server status OK

        else
            Log.d(TAG, "Server Response Failure!");

        return token;
    } // handleResponse()



    @Override
    protected void onPostExecute(String token) {
        Log.d(TAG, "storing token :" + token);

        SharedPreferences prefs = context.getSharedPreferences(
                TabActivity.PACKAGE_NAME, Context.MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();

        // if token doesn't already exist or it is old
        if (!prefs.contains("token") || !prefs.getString("token", "").equals(token))
                editor.putString("token", token);

        editor.apply();
    } // onPostExecute
} // class uploadAsync