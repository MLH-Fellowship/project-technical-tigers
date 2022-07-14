window.onload = async () => {
    await fetch("/api/timeline_post")
    .then((resp) => resp.json())
    .then((data) => {
        const posts = data.timeline_posts
        for(let i=0; i < posts.length; i++){
            let currentPost = posts[i];
            document.getElementById("posts").innerHTML += 
            "<div class=\"card my-5\">" +
                "<div class=\"card-header\">" + 
                    currentPost.name + 
                "</div>" +
                "<div class=\"card-body\">" + 
                    "<blockquote class=\"blockquote mb-0\">" +
                        "<p>" + currentPost.content + "</p>" +
                    "<footer class=\"blockquote-footer\">" + currentPost.email + "<cite> Created at: "  + currentPost.created_at + "</cite></footer>" + 
                    "</blockquote>" + 
                "</div>" + 
            "</div>"
        }
    })
}


let postFormData = async(e) => {
    e.preventDefault();

    const form = document.getElementById('timeLine-posts-form');
    const formData = new FormData(form);

    try {
        await fetch('/api/timeline_post', {
            method: 'POST',
            body: formData
        })

    } catch (err) {
        console.log('An error occured', err);
    } finally {
        location.reload()
    }
}   