package com.example.fitbit;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.jar.Attributes;

public class CallAPI extends AsyncTask<String, String, String> {
    AsyncResponse responseFunction;
    String method;
    public CallAPI(String method,AsyncResponse responseFunction){
        this.responseFunction=responseFunction;
        this.method=method;
        //set context variables if required
    }

    @Override
    protected void onPostExecute(String result) {
        responseFunction.processFinish(result);
    }

    @Override
    protected void onPreExecute() {
        super.onPreExecute();
    }

    @Override
    protected String doInBackground(String... params) {
        String urlString = params[0]; // URL to call
        String data = params[1]; //data to post
        OutputStream out = null;
        String response=null;
        try {
            URL url = new URL(urlString);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.setRequestMethod(method);
            urlConnection.setDoInput(true);
            urlConnection.setDoOutput(true);
            urlConnection.setRequestProperty("Content-Type", "application/json; utf-8");
            urlConnection.setRequestProperty("Accept", "application/json");
            out = new BufferedOutputStream(urlConnection.getOutputStream());

            BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
            writer.write(data);
            writer.flush();
            writer.close();
            out.close();

            urlConnection.connect();
            StringBuilder sb = new StringBuilder();
            BufferedReader br = new BufferedReader(new InputStreamReader((urlConnection.getInputStream())));
            String output=null;
            while ((output = br.readLine()) != null) {
                sb.append(output);
            }
            response=sb.toString();
            Log.d("TEST","response_code:"+urlConnection.getResponseCode());
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return response;
    }
}