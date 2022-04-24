function edit(elem) {
    var element = elem

    const textarea = document.createElement("textarea");
    textarea.setAttribute("id", "jstextarea");

    const jsbutton = document.createElement("button");
    jsbutton.innerHTML = "Submit Edit!";
    jsbutton.setAttribute("id", "jseditbutton");
    jsbutton.setAttribute("class", "btn btn-danger");
    
    parent = element.parentNode;
    var text = parent.querySelector('p');
    textarea.innerHTML = text.textContent;

    text.replaceWith(textarea);
    element.replaceWith(jsbutton);

    btn = document.querySelector('#jseditbutton');
    ta = document.querySelector('#jstextarea');

    btn.addEventListener('click', () => 


    fetch(`/index/`, {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            id: text.id,
            content: ta.value,
        }),
        mode : 'same-origin' // For same origin requests 
    })
    .then(response => response.text())
    .then(response => {
        jsbutton.replaceWith(elem)
        text.innerHTML = ta.value 
        textarea.replaceWith(text) 
    }));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function like(likebutton) {
    var e = likebutton

    post = e.parentNode
    postid = post.querySelector('p').id
    
    likes = post.querySelector('#PostLikes')
    likesstring = likes.innerHTML
    var num = likesstring.replace(/[^0-9]/g,'');
    likesint = parseInt(num)


    fetch(`/index/`, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            desiredaction: e.innerHTML,
            id: postid,
        }),
        mode : 'same-origin'
    })
    .then(response => response.text()
    .then(response => {
        if (e.innerHTML == "Like") {
            e.innerHTML = "Unlike";
            likesstring = "Likes: " + (likesint+1);
            const newlikes = document.createElement('p')
            newlikes.setAttribute("id", "PostLikes")
            newlikes.innerHTML = likesstring
            likes.replaceWith(newlikes)
        } else if (e.innerHTML == "Unlike") {
            e.innerHTML = "Like";
            likesstring = "Likes: " + (likesint-1)
            const newlikes = document.createElement('p')
            newlikes.setAttribute("id", "PostLikes")
            newlikes.innerHTML = likesstring
            likes.replaceWith(newlikes)
        }
    }));
}


    
    
