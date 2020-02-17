package com.example.fitbit;

import android.os.Looper;
import android.os.Handler;
import android.os.Message;
import android.util.Log;
import com.example.fitbit.model.Metrics;
import com.example.fitbit.model.User;

import org.json.JSONObject;
import java.util.Date;
import java.util.ArrayList;

class DummyLooper{
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
        ArrayList<Metrics> metrics= new ArrayList();
        metrics.add(new Metrics("heart",new Date().getTime(),(Math.random() * 30) + 80));
        metrics.add(new Metrics("calories",new Date().getTime(),(Math.random() * 20) + 10));
        Log.d("metrics",metrics.toString());
        String username = User.findAll(User.class).next().getUsername();
        request.execute(Urls.SERVER_URL + Urls.INSERT_METRICS_ENDPOINT,
                        "metrics", metrics.toString(),
                        "username", username);
    }
}
