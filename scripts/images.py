import os
import re
import shutil
import logging

# Paths (using raw strings to handle Windows backslashes correctly)
# Correct the paths depending on your system
posts_dir = r"D:\Vaults\Regular(Main)\Blog\temp"
attachments_dir = r"D:\Vaults\Regular(Main)\Blog\posts\attachments"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        file_dir = os.path.join(posts_dir, filename.replace(".md", ""))
        
        img_dir = os.path.join(file_dir, "img")
        os.makedirs(img_dir, exist_ok=True)
        
        filepath = os.path.join(file_dir, "index.md")
        os.rename(os.path.join(posts_dir, filename), filepath)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
        images = re.findall(r'!\[\[([^]]*\.(?:png|jpg|jpeg|gif|bmp|webp))\]\]', content)

        featured = [image for image in images if image.find("feature") != -1]
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            if image in featured:
                content = content.replace(f"![[{image}]]", "")
            else:
                # Prepare the Markdown-compatible link with %20 replacing spaces
                new_image_name = image.replace(' ', '_')
                markdown_image = f"![Image Description](/img/{new_image_name})"
                content = content.replace(f"![[{image}]]", markdown_image)
                

                # Step 4: Copy the image to the Hugo static/images directory if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, img_dir)
                    os.rename(os.path.join(img_dir, image), os.path.join(img_dir, new_image_name))
                else:
                    raise Exception(f"Image file does not exist: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        if len(featured) > 1:
            raise Exception(f"More than one feature found limit of 1 feature exceeded: {featured}")
        elif len(featured) == 1:
            shutil.copy(os.path.join(attachments_dir, featured[0]), file_dir)

logging.info("Markdown files processed and images copied successfully.")
