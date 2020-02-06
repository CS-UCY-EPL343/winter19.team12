package com.example.fitbit;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

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

        JSONObject object = new JSONObject();
        try {
            Map<String, String> files = new HashMap<String, String>();
            Method method = session.getMethod();
            if (Method.PUT.equals(method) || Method.POST.equals(method)) {
                try {
                    session.parseBody(files);
                } catch (IOException ioe) {
                    ioe.printStackTrace();
                } catch (ResponseException re) {
                    re.printStackTrace();
                }
            }

            if (session.getParameters().get("MsgType").get(0) == null) {
                object.put("Result", "Missing MsgType");
                Log.v(TAG, "Missing MsgType");

            } else {
                if (session.getParameters().get("Msg").get(0) == null) {
                    object.put("Result", "Missing Msg");
                    Log.v(TAG, "Missing Msg");
                } else {
                    Log.v(TAG, session.getParameters().get("Msg").get(0));
                    //JSONObject result = ;
//                    if(result != null)
//                        object.put("Result", result);
//                    else
//                        object.put("Result", "Errors processing data!");
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        }

        return newFixedLengthResponse(object.toString());
    }
}