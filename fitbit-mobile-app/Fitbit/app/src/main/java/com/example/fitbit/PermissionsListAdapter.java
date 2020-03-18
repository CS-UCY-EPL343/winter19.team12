package com.example.fitbit;

import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.TextView;

public class PermissionsListAdapter extends ArrayAdapter {
    //to reference the Activity
    private final Activity context;

    //to store the list of names
    private final String[] nameArray;

    //to store the list of emails
    private final String[] secondaryArray;

    public PermissionsListAdapter(Activity context, String[] nameArray, String[] secondaryArray){
        super(context,R.layout.list_permission_row , nameArray);
        this.context=context;
        this.nameArray=nameArray;
        this.secondaryArray =secondaryArray;

    }
    public View getView(int position, View view, ViewGroup parent) {
        LayoutInflater inflater=context.getLayoutInflater();
        View rowView=inflater.inflate(R.layout.list_permission_row, null,true);

        //this code gets references to objects in the listview_row.xml file
        TextView nameTextField = rowView.findViewById(R.id.textDoctorName);
        TextView emailTextField = rowView.findViewById(R.id.textDoctorMail);
        ImageView imageView = rowView.findViewById(R.id.imageReject);

        if(secondaryArray[position].equals("Request Accepted")||secondaryArray[position].equals("Pending Acceptance")){
            imageView.setImageResource(R.drawable.ic_cancel);
        }

        //this code sets the values of the objects to values from the arrays
        nameTextField.setText(nameArray[position]);
        emailTextField.setText(secondaryArray[position]);
        return rowView;
    }

}
