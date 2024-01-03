# shopping

This is a flask website used to link to products at our local supermarkets. You can link to whatever you want.

To use.....

    docker run -d \
      --name shopping \
      --restart always \
      -p 80:80 \
      -v /data_dir:/app/data:z \
      -e TZ=Pacific/Auckland \
      skippynz/shopping:latest

Create one directories: data

Inside the data directory, a database will be created automatically the first time you run. Add products from the link in the top right corner. You can edit and delete items as required.

Feel free to create an issue if you want to discuss anything.
