package com.example.fitbit;

import android.util.Log;

import com.example.fitbit.model.Metrics;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

import fi.iki.elonen.NanoHTTPD;

public class Nano extends NanoHTTPD {
    private static final String TAG = "Nano";

    public Nano(int port) throws IOException {
        super(port);
        start(NanoHTTPD.SOCKET_READ_TIMEOUT, true);
        System.out.println("\nRunning! Point your browsers to http://localhost:" + port + "/ \n");
    }

    @Override
    public NanoHTTPD.Response serve(IHTTPSession session) {
        Log.d("server_test", "Server received!");
        JSONObject result = new JSONObject();
        Method method = session.getMethod();

        try {
//            Map<String, String> files = new HashMap<String, String>();
//            if (Method.PUT.equals(method) || Method.POST.equals(method)) {
//                try {
//                    session.parseBody(files);
//                } catch (IOException | ResponseException ioe) {
//                    ioe.printStackTrace();
//                }
//            }
            if (Method.GET.equals(method)) {
                try {

                    String type = session.getParameters().get("type").get(0);
                    String value = session.getParameters().get("value").get(0);
                    if (value.equals("undefined")) {
                        return newFixedLengthResponse(result.put("Error", "value undefined").toString());
                    }
                    double actual_value = Double.parseDouble(value);
                    Date now = new Date();
                    Metrics metrics = new Metrics(type, now.getTime(), actual_value);
                    metrics.save();
                    result.put("Code", 1);
                    Log.v(TAG, "metric type:" + type + " value:" + value);
                } catch (Exception ex) {
                    Log.v(TAG, "Missing Get Params");
                    Log.v(TAG, Objects.requireNonNull(ex.getMessage()));
                    result.put("Error", 1);
                }
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }

        return newFixedLengthResponse(result.toString());
    }
}