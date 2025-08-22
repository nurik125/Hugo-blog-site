import os
import re
import shutil
import logging

# Paths (using raw strings to handle Windows backslashes correctly)
# Correct the paths depending on your system
posts_dir = r"D:\Vaults\Regular(Main)\Blog\temp"
attachments_dir = r"D:\Vaults\Regular(Main)\Blog\posts\attachments"

# Relative var
static_images_dir = r"static\images"

# Step 1: Process each markdown file in the posts directory
for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
        images = re.findall(r'!\[\[([^]]*\.(?:png|jpg|jpeg|gif|bmp|webp))\]\]', content)

        featured = [image for image in images if image.find("feature") != -1]
        
        # Step 3: Replace image links and ensure URLs are correctly formatted
        for image in images:
            if image in featured:
                markdown_image = ""
                content = content.replace(f"![[{image}]]", markdown_image)
            else:
                # Prepare the Markdown-compatible link with %20 replacing spaces
                markdown_image = f"![Image Description](/images/{image.replace(' ', '%20')})"
                content = content.replace(f"![[{image}]]", markdown_image)
                
                # Step 4: Copy the image to the Hugo static/images directory if it exists
                image_source = os.path.join(attachments_dir, image)
                if os.path.exists(image_source):
                    shutil.copy(image_source, static_images_dir)
                else:
                    raise Exception(f"Image file does not exist: {image_source}")

        # Step 5: Write the updated content back to the markdown file
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(content)

        if len(featured) > 1:
            raise Exception(f"More than one feature found limit of 1 feature exceeded: {featured}")
        elif len(featured) == 1:
            new_post_dir = os.path.join(posts_dir, filename[:-3]+"\\")
            os.makedirs(new_post_dir, exist_ok=True)
            new_filepath = os.path.join(posts_dir, "index.md")
            if not(os.path.exists(new_filepath)):
                os.rename(filepath, new_filepath)
                shutil.move(new_filepath, new_post_dir)
                shutil.copy(os.path.join(attachments_dir, featured[0]), new_post_dir)
            else:
                raise Exception(f"File index.md already exists in {posts_dir}" + FileExistsError)

logging.info("Markdown files processed and images copied successfully.")
