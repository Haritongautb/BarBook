$(document).ready(function(){
    const header = $("#header");
    const deleteAllPostsBtn = $("#delete-all-posts");

    function headerFixed(){
        if(!header){
            return;
        }
        $(window).scroll(function(){
          if($(this).scrollTop() > 0){
            header.css({"position": "fixed"})
          } else {
            header.css({"position": "static"})
          }
        })
    }

    headerFixed();

    function postsJSON(){
        const formJSON = $('#json-form');
        if(!!formJSON){
            async function request(event){
                event.preventDefault();

                const formData = new FormData(event.target);
                const fields = Object.fromEntries(formData);

                const response = await fetch("http://127.0.0.1:5000/createByJSON", {
                    method: "POST",
                    body: JSON.stringify(fields),
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8'
                    }
                })

                    const result = await response.json();
                    console.log(result);
            }
//            formJSON[0].addEventListener("submit", request);
        } else {
            return;
        }
    }

    postsJSON();

    deleteAllPostsBtn.click(function(){
        const buttonsBlock = `
            <div id="buttons-block">
                <button id="btn-confirm-delete-all" type="submit">Confirm</button>
                <button id="btn-cancel-delete-all">Cancel</button>
            </div>
        `
        const allPosts = $("form");
        let hasInput;

        allPosts.eq(0).children().each(function(index, element){
            if(!$(element).attr("data-type")){
                hasInput = false;
            } else {
                hasInput = true;
            }
        })

        if(!hasInput){
            allPosts.each(function(index, element){
                $(element).append($('<input>', {'type': 'checkbox', "checked": true, 'data-type': "checkbox"}));
            })
            $(this).after(buttonsBlock)
            confirmDeleteAll()
            cancelDeleteAll();
        } else {
            allPosts.each(function(index, element){
                $(element).find('[data-type="checkbox"]').remove();
            })
            $('#buttons-block').remove();
        }
    })

    function confirmDeleteAll(){
        $("#btn-confirm-delete-all").click(function(event){
            event.preventDefault();
            const usersIDs = [];

            $("form").each(function(index, element){
                usersIDs.push($(element).find('[name="id"]').val());
            })

            const json = JSON.stringify({"ids": usersIDs});

            async function deleteAllRequest(){
            console.log(json)
                const response = await fetch("http://127.0.0.1:5000/deleteAll", {
                    method: "POST",
                    body: json,
                    headers: {
                        'Content-Type': 'application/json;charset=utf-8'
                    }
                })
                const result = await response.json();

                console.log(result);
            }
            deleteAllRequest();
        })
    }

    function cancelDeleteAll(){
        const btnCancelDeleteAll = $("#btn-cancel-delete-all");

        btnCancelDeleteAll.click(function(){
            $("form").each(function(index, element){
                $(element).find('[data-type="checkbox"]').remove();
            })
            $('#buttons-block').remove();
        })


    }


})