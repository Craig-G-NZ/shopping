# shopping

This is a flask website used to link to products at our local supermarkets. You can link to whatever you want.

To use.....

    docker run -d \
      --name shopping \
      --restart always \
      -p 80:80 \
      -v /data_dir:/app/data:z \ #optional
      -e TZ=Pacific/Auckland \
      skippynz/shopping:latest

Optional: Create a directory and name it whatever you want e.g. data_dir - this will be used above in your docker command for the volume (-v). An empty database will be automatically created in the "data_dir" folder. If you want change the name and title of the website, you will need to create a config.json file in the data_dir folder with the following content. Change as you see fit. If you dont create the file it might self name to "Default Title" and "Default Name".
    
    {
    "website_title": "Product Links",
    "website_name": "Product Links"
    }   
    
Feel free to create an issue if you want to discuss anything.
