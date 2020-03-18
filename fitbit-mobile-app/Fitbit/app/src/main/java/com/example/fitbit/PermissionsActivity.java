package com.example.fitbit;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;

import com.example.fitbit.model.User;
import com.google.gson.JsonObject;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.concurrent.ExecutionException;

public class PermissionsActivity extends AppCompatActivity {

    String[] nameArray;
    String[] secondaryArray;
    String[] username;

    ListView listView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_permissions);

        HashMap<String,String> headers = new HashMap<>();
        headers.put("Authorization", "Bearer " + User.first(User.class).getToken());
        CallAPI fetchRequest=new CallAPI("GET",headers,null);

        try {
            String r=fetchRequest.execute(Urls.SERVER_URL + Urls.PERMISION_REQUEST).get();
            JSONObject results = new JSONObject(r);
            JSONArray specialistsSend=results.getJSONArray("specialists_sent");
            JSONArray specialistsNotSend=results.getJSONArray("specialists_not_sent");
            nameArray=new String[specialistsNotSend.length()+specialistsSend.length()];
            secondaryArray=new String[specialistsNotSend.length()+specialistsSend.length()];
            username=new String[specialistsNotSend.length()+specialistsSend.length()];

            for(int i=0;i<specialistsSend.length();i++){
                JSONObject specialist=specialistsSend.getJSONObject(i);
                nameArray[i]=specialist.getString("first_name")+specialist.getString("last_name");
                username[i]=specialist.getString("username");
                secondaryArray[i]=specialist.getBoolean("completed")?"Request Accepted":"Pending Acceptance";
            }
            for(int i=0;i<specialistsNotSend.length();i++){
                JSONObject specialist=specialistsNotSend.getJSONObject(i);
                nameArray[specialistsSend.length()+i]=specialist.getString("first_name")+specialist.getString("last_name");
                username[specialistsSend.length()+i]=specialist.getString("username");
                secondaryArray[specialistsSend.length()+i]=specialist.getString("telephone");
            }
        } catch (ExecutionException |InterruptedException|JSONException e) {
            Log.d("PERMISSION_LIST",e.getMessage());
            e.printStackTrace();
        }

        PermissionsListAdapter listAdapter=new PermissionsListAdapter(this,nameArray,secondaryArray);

        listView = findViewById(R.id.list_permission);
        listView.setAdapter(listAdapter);

        listView.setOnItemClickListener((parent,view,position,id)->{
            Log.v("ListListener","Inside listener");
            if(secondaryArray[position].equals("Request Accepted")||secondaryArray[position].equals("Pending Acceptance")){
                new AlertDialog.Builder(this).setTitle("Revoke Permissions")
                        .setMessage("Do you want this doctor to not be able to view your data")
                        .setPositiveButton(android.R.string.yes,(d,w)->{
                            //TODO cancel the request or revoke access
                        })
                        .setNegativeButton(android.R.string.no,null)
                        .setIcon(null)
                        .show();

            }else{
                new AlertDialog.Builder(this).setTitle("Give Access Permissions")
                        .setMessage("Do you want "+nameArray[position]+" to be able to view your data")
                        .setPositiveButton(android.R.string.yes,(d,w)->{
                            CallAPI request=new CallAPI("POST",headers,(r)->{
                                try{
                                    JSONObject results=new JSONObject(r);
                                    View child=listView.getChildAt(position);
                                    if(child==null){
                                        return;
                                    }
                                    TextView textInfo=child.findViewById(R.id.textDoctorMail);
                                    textInfo.setText(R.string.pending_acceptance);
                                    ImageView imageView=child.findViewById(R.id.imageReject);
                                    imageView.setImageResource(R.drawable.ic_cancel);
                                }catch (JSONException ex){
                                    Log.d("PERMISSION_LIST",ex.getMessage());
                                    ex.printStackTrace();
                                }
                            });
                            request.execute(Urls.SERVER_URL+Urls.PERMISION_REQUEST,"username",username[position]);
                        })
                        .setNegativeButton(android.R.string.no,null)
                        .setIcon(null)
                        .show();
            }
        });
    }
}
