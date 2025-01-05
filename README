# ExploreBlog Project

## Project Overview
ExploreBlog is a blogging platform where users can:

- Create, edit, and manage their blogs.
- View blogs written by others, along with metadata like views, creator, and creation date.
- Access a "Home" tab to view all blogs.
- Use the "My Blogs" tab to view their created blogs.
- Update their profile details in the "Profile" section.
- Request edit access to other users' blogs and edit them once access is granted.
- Manage incoming and outgoing access requests.

This project is built using Django's MTV (Model-Template-View) architecture and is containerized for flexible deployment.

---

## Features
### Blog Management
- **Create Blogs:** Users can write and publish blogs.
- **View Blogs:** All blogs are accessible on the "Home" tab.
- **My Blogs Tab:** Users can see and manage blogs they have created.
- **Blog Metadata:** Each blog displays its views, creator, and creation date.

### Profile Management
- **Profile Updates:** Users can update their personal details.

### Edit Requests
- **Request Access:** Users can request edit access to others' blogs.
- **Grant Access:** Blog owners can manage incoming requests and grant access.
- **One-Time Edit:** Granted access allows one-time editing only.
- **Request Management:**
  - View incoming requests for blog access.
  - View all blogs for which the user has requested access.

---

## Projects Images
![My Blogs](ExploreBlogApp/ExploreBlog/media/assets/my_blogs.png)
![Create Blog](ExploreBlogApp/ExploreBlog/media/assets/create_blog.png)
![Blog Page](ExploreBlogApp/ExploreBlog/media/assets/blog_view.png)
![I Requested Blog Access](ExploreBlogApp/ExploreBlog/media/assets/i_requested.png)
![Requested My Access](ExploreBlogApp/ExploreBlog/media/assets/requested_me.png)

---

## Installation

### Prerequisites
- Docker and Docker Compose installed.

### Clone the Repository
```bash
git clone https://github.com/SanthoshBoggala/ExploreBlogApp.git
cd ExploreBlogApp
```

### Build and Run with Docker Compose
#### Using SQLite3 (Default)
1. Start the containers:
   ```bash
   docker-compose -f docker-compose-sqlite3.yml up --build -d
   ```
2. Access the application at `http://localhost:9091`.

#### Using PostgreSQL
1. Start the containers with PostgreSQL:
   ```bash
   docker-compose -f docker-compose-postgresql.yml up --build -d
   ```
2. Access the application at `http://localhost:9090`.

---

## Architecture
This project follows the Django MTV (Model-Template-View) pattern:

- **Models:** Define database schema for users, blogs, and access requests.
- **Templates:** Render the front-end HTML.
- **Views:** Handle HTTP requests and responses.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.