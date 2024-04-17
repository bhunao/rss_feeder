{% extends "base.html" % }
{% block content % }

<div >
    <h1 > Feed < /h1 >
</div >

{% for item in list_feed % }
<div class = "card mb-3" >
   <div class = "row g-0" >
       <div class = "col-md-4 text-center" >
            {% if item.media_content % }
            <img src = "{{ item.media_content }}" class = "img-thumbnail img-fluid rounded-0" >
            {% else % }
            <img src = "https://dummyimage.com/350x200" class = "img-thumbnail img-fluid rounded-0" >
            {% endif % }
        </div >
        <div class = "col-md-8 card-body" >
           <div class = "row align-items-start" >
               <div class = "col-1" >
                    <h3 > <i class = "bi bi-person-circle"></i></h3>
                </div >
                <div class = "col" >
                    <span class = "align-text-bottom" > {{ item.feed_id }}</span>
                </div >
                <div class = "col text-end" >
                    <span class = "align-text-bottom" > {{ item.published }}</span>
                </div >
            </div >

            <h5 class = "card-title" > {{ item.title }}</h5>
            <p class = "card-text text-truncate" > {{ item.summary }}</p>

            <a href = "{{ item.link }}" class = "btn btn-outline-primary border-0 rounded-0 py-2 icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.4rem, 0);" href="#">
            Ler no site
            </a >
            <a href = "#" class = "btn btn-outline-primary border-0 rounded-0 py-2 icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.4rem, 0);" href="#">
                <i class = "bi bi-hand-thumbs-up" > </i>
            </a >
            <a href = "#" class = "btn btn-outline-primary border-0 rounded-0 py-2 icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.4rem, 0);" href="#">
                <i class = "bi bi-hand-thumbs-down" > </i>
            </a >
            <a href = "#" class = "btn btn-outline-primary border-0 rounded-0 py-2 icon-link icon-link-hover" style="--bs-icon-link-transform: translate3d(0, -.4rem, 0);" href="#">
                <i class = "bi bi-share" > </i>
            </a >
        </div >
    </div >
</div >
{ % endfor % }

{ % endblock % }
