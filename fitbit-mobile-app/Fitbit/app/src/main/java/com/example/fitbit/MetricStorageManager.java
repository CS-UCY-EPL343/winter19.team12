package com.example.fitbit;

import android.os.Handler;
import android.util.Log;

import com.example.fitbit.model.Metrics;
import com.example.fitbit.model.User;
import com.orm.query.Select;

import org.json.JSONObject;

import java.util.List;

public class MetricStorageManager {
    private Handler mHandler = new Handler();
    public static final int BATCH_SIZE=200;//how many metrics can be sent simultaneously
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            if(NetworkChangeReceiver.hasInternetConnectivity()){
                sendMetrics();
            }
            mHandler.postDelayed(this, 5000);
        }
    };
    public void storeMetrics(List<Metrics> metrics){
        if(!NetworkChangeReceiver.hasInternetConnectivity()){
            for(Metrics item:metrics){
                item.save();
            }
        }
        else{
            CallAPI request = new CallAPI("POST", output -> {
                try {
                    JSONObject obj = new JSONObject(output);
                    Log.d("DUMMY", obj.toString());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
            request.execute(Urls.SERVER_URL + Urls.INSERT_METRICS_ENDPOINT,
                            "metrics",metrics.toString(),
                            "username", User.findAll(User.class).next().getUsername());
        }
    }
    public void start(){
        mHandler.postDelayed(runnable,5000);
    }
    public void stop(){
        mHandler.removeCallbacks(runnable);
    }
    public void sendMetrics() {
        //while there are metrics waiting to be sent and there is internet connection
        while(Metrics.count(Metrics.class)>0 && NetworkChangeReceiver.hasInternetConnectivity()){
            List<Metrics> metricRecords = Select.from(Metrics.class)
                                                .orderBy("timestamp DESC")
                                                .limit(String.valueOf(BATCH_SIZE))
                                                .list();
            CallAPI request = new CallAPI("POST", output -> {
                try {
                    JSONObject obj = new JSONObject(output);
                    if(obj.has("status") && obj.get("status").equals("1")){
                        //metrics successfuly sent to server,delete the batch android SQLite
                        for(Metrics item:metricRecords){
                            Metrics.delete(item);
                        }
                    }
                    Log.d("DUMMY", obj.toString());
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
            request.execute(Urls.SERVER_URL + Urls.INSERT_METRICS_ENDPOINT, "metrics",metricRecords.toString());
        }

    }
}
