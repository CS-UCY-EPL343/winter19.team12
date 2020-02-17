package com.example.fitbit;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.EditText;
import android.widget.Toast;

import com.example.fitbit.model.User;

import org.json.JSONException;
import org.json.JSONObject;

public class ChangePasswordActivity extends AppCompatActivity {
    private EditText oldPassword;
    private EditText newPassword;
    private EditText rePassword;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_change_password);
        oldPassword=findViewById(R.id.editTextOldPasswordChangePassword);
        newPassword=findViewById(R.id.editTextPasswordChangePassword);
        rePassword=findViewById(R.id.editTextRePasswordChangePassword);
        findViewById(R.id.changePasswordSumbit).setOnClickListener((l)->{
            CallAPI changePass=new CallAPI("POST",(r)->{
                JSONObject results;
                try{
                    results=new JSONObject(r);
                    if(results.has("error")){
                        if(results.getString("error").equals("user not found")){
                            Toast.makeText(ChangePasswordActivity.this,"Wrong Password!",Toast.LENGTH_SHORT).show();
                        }
                    }
                    if(results.getString("status").equals("1")){
                        Toast.makeText(ChangePasswordActivity.this,"Changed password successful!",Toast.LENGTH_SHORT).show();
                        Intent myIntent = new Intent(ChangePasswordActivity.this, MainActivity.class);
                        startActivity(myIntent);
                    }
                }catch (JSONException e){
                    e.printStackTrace();
                    Toast.makeText(ChangePasswordActivity.this,"Something went wrong: "+e.getMessage(),Toast.LENGTH_SHORT).show();
                }
            });
            if(newPassword.getText().toString().equals("")){
                newPassword.setError("You must provide a password");
                return;
            }else if(!newPassword.getText().toString().equals(rePassword.getText().toString())){
                rePassword.setError("Password are not matching");
                return;
            }
            User user= User.first(User.class);
            changePass.execute(Urls.SERVER_URL+Urls.CHANGE_PASSWORD_ENDPOINT,
                    "username",user.getUsername(),
                    "old_password",oldPassword.getText().toString(),
                    "password_new",newPassword.getText().toString(),
                    "repeat_password",rePassword.getText().toString());
        });
    }
}
