package com.example.fitbit;

import android.os.Handler;
import android.util.Log;

import com.example.fitbit.model.Metrics;
import com.example.fitbit.model.User;
import com.orm.query.Select;

import org.json.JSONObject;

import java.util.List;

public class MetricStorageManager {
    public static final String TAG = "MetricStorageManager";
    private Handler mHandler = new Handler();
    public static final int DB_CHECK_TIME=2000;
    public static final int BATCH_SIZE=200;//how many metrics can be sent simultaneously
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            if(User.count(User.class)==0){
                Log.d(TAG,"No user to send metrics");
                return;
            }
            if(NetworkChangeReceiver.hasInternetConnectivity()){
                sendMetrics();
            }
            mHandler.postDelayed(this, DB_CHECK_TIME);
        }
    };
    public static void storeMetrics(String type,long timestamp,double amount){
        Metrics metric = new Metrics(type,timestamp,amount);
        metric.save();
    }
    public void start(){
        Log.d("handler_started","handler_start");
        mHandler.postDelayed(runnable,DB_CHECK_TIME);
    }
    public void stop(){
        if(mHandler!=null && runnable!=null) {
            Log.d(TAG,"removed");
            mHandler.removeCallbacks(runnable);
        }
    }
    public void sendMetrics() {
        Log.d("METRICS","Metrics remaining:"+String.valueOf(Metrics.count(Metrics.class)));
        //while there are metrics waiting to be sent and there is internet connection
        List<Metrics> metricRecords = Select.from(Metrics.class)
                                            .orderBy("timestamp DESC")
                                            .limit(String.valueOf(BATCH_SIZE))
                                            .list();
        CallAPI request = new CallAPI("POST", output -> {
            try {
                JSONObject obj = new JSONObject(output);
                Log.d("res",obj.toString());
                if(obj.has("status") && obj.get("status").equals("1")){
                    //metrics successfuly sent to server,delete the batch android SQLite
                    for(Metrics item:metricRecords){
                        item.delete();
                    }
                    //We call again send metric function if there are still data to be sent
                    if(Metrics.count(Metrics.class)>0 && NetworkChangeReceiver.hasInternetConnectivity()){
                        sendMetrics();
                    }
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
        request.execute(Urls.SERVER_URL + Urls.INSERT_METRICS_ENDPOINT, "metrics",metricRecords.toString(),
                        "username",User.first(User.class).getUsername());


    }
}
