package com.example.fitbit;

import android.os.Looper;
import android.os.Handler;
import android.os.Message;
import android.util.Log;

import org.json.JSONObject;

class DummyLooper{
    private static final String INSERT_METRICS_ENDPOINT = "/insert_metrics";
    private Handler mHandler = new Handler();
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            dummyPost();
            mHandler.postDelayed(this, 2000);
        }
    };
    public void start(){
        mHandler.postDelayed(runnable,2000);
    }
    public void stop(){
        mHandler.removeCallbacks(runnable);
    }
    public void dummyPost() {

        CallAPI request = new CallAPI("POST", output -> {
            try {
                JSONObject obj = new JSONObject(output);
                Log.d("DUMMY", obj.toString());
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        String value = String.valueOf((int) (Math.random() * 30) + 80);
        request.execute(Urls.SERVER_URL + INSERT_METRICS_ENDPOINT, "type", "heart", "value", value);
    }
}
