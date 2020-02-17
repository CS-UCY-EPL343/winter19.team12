package com.example.fitbit;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.util.Log;

public class NetworkChangeReceiver extends BroadcastReceiver {
    private static boolean isConnected;
    @Override
    public void onReceive(final Context context, final Intent intent) {

        int status = NetworkUtil.getConnectivityStatusString(context);
        if ("android.net.conn.CONNECTIVITY_CHANGE".equals(intent.getAction())) {
            if (status == NetworkUtil.NETWORK_STATUS_NOT_CONNECTED) {
                Log.d("conn","not connected");
                isConnected=false;
            } else {
                Log.d("conn","connected");
                isConnected=true;
            }
        }
    }
    public static boolean hasInternetConnectivity(){
        return isConnected;
    }
}