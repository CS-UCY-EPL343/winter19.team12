package com.example.fitbit;

import androidx.appcompat.app.AppCompatActivity;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.Toast;

import com.example.fitbit.model.User;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Calendar;

public class EditProfile extends AppCompatActivity {
    private final String EDIT_PROFILE_ENDPOINT="/edit_profile_api";
    private final String VIEW_PROFILE_DETAILS="/get_user_info";

    private EditText name;
    private EditText surname;
    private EditText birthday;
    private EditText height;
    private RadioButton isMale;
    private RadioButton isFemale;
    private EditText email;
    private EditText phone;
    private EditText address;
    private EditText weight;

    private int mYear, mMonth, mDay;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_profile);
        name=findViewById(R.id.editTextNameEditProfile);
        surname=findViewById(R.id.editTextSurnameEditProfile);
        birthday=findViewById(R.id.editTextBirthdayEditProfile);
        birthday.setOnClickListener((l)->{
            final Calendar c = Calendar.getInstance();
            mYear = c.get(Calendar.YEAR);
            mMonth = c.get(Calendar.MONTH);
            mDay = c.get(Calendar.DAY_OF_MONTH);
            DatePickerDialog datePickerDialog = new DatePickerDialog(this,
                    (view, year, monthOfYear, dayOfMonth) -> birthday.setText(dayOfMonth + "/" + (monthOfYear + 1) + "/" + year), mYear, mMonth, mDay);
            datePickerDialog.show();
        });
        height=findViewById(R.id.editTextHeightEditProfile);
        isMale=findViewById(R.id.radioButtonIsMaleEditProfile);
        isFemale=findViewById(R.id.radioButtonIsFemaleEditProfile);
        email=findViewById(R.id.editTextEmailEditProfile);
        phone=findViewById(R.id.editTextTelephoneEditProfile);
        address=findViewById(R.id.editTextAddressEditProfile);
        weight=findViewById(R.id.editTextWeightEditProfile);


        CallAPI userInfo=new CallAPI("POST",(r)->{
            try {
                JSONObject results=new JSONObject(r);
                height.setText(results.getString("height").equals("null")?"":results.getString("height"));
                birthday.setText(results.getString("birthdate").equals("null")?"":results.getString("birthdate"));
                name.setText(results.getString("first_name").equals("null")?"":results.getString("first_name"));
                surname.setText(results.getString("last_name").equals("null")?"":results.getString("last_name"));
                email.setText(results.getString("email").equals("null")?"":results.getString("email"));
                phone.setText(results.getString("telephone").equals("null")?"":results.getString("telephone"));
                address.setText(results.getString("address").equals("null")?"":results.getString("address"));
                weight.setText(results.getString("weight").equals("null")?"":results.getString("weight"));
                if(results.getString("gender").equals("Male")){
                    isMale.setChecked(true);
                    isFemale.setChecked(false);
                }else if(results.getString("gender").equals("Female")){
                    isMale.setChecked(false);
                    isFemale.setChecked(true);
                }

            } catch (JSONException e) {
                e.printStackTrace();
            }

        });
        User currentUser=User.first(User.class);
        userInfo.execute(Urls.SERVER_URL+VIEW_PROFILE_DETAILS,"username",currentUser.getUsername());

        findViewById(R.id.buttonEditProfileSubmit).setOnClickListener((l)->{
            CallAPI userDataChange = new CallAPI("POST",(r)->{
                try{
                    JSONObject results=new JSONObject(r);
                    if(results.getString("status").equals("1")){
                        Toast.makeText(EditProfile.this,"Edit profile successful!",Toast.LENGTH_SHORT).show();
                        Intent myIntent = new Intent(EditProfile.this, MainActivity.class);
                        startActivity(myIntent);
                    }
                }catch (JSONException e){
                    e.printStackTrace();
                    Toast.makeText(EditProfile.this,"Something went wrong: "+e.getMessage(),Toast.LENGTH_SHORT).show();
                }
            });

            userDataChange.execute(Urls.SERVER_URL+EDIT_PROFILE_ENDPOINT,
                    "username",currentUser.getUsername(),
                    "first_name",name.getText().toString(),
                    "last_name",surname.getText().toString(),
                    "birthday",mDay+"/"+mMonth+"/"+mYear,
                    "height",height.getText().toString(),
                    "gender",isMale.isChecked()?"Male":"Female",
                    "email",email.getText().toString(),
                    "telephone",phone.getText().toString(),
                    "address",address.getText().toString(),
                    "weight",weight.getText().toString());
        });
    }
}
