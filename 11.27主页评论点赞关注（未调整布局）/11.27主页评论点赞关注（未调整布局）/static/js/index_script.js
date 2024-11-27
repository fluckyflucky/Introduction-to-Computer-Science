// 切换主题的函数
function toggleTheme() {
    document.body.classList.toggle('dark-mode'); // 直接切换主题
}

window.onload = function() {
    var mainContent = document.querySelector('.main-content');
    mainContent.classList.add('fade-in'); // 添加入场动画类
};

// 放大后显示的内容数组
const expandedTexts = [
    '这是放大的内容1',
    '这是放大的内容2',
    '这是放大的内容3',
    '这是放大的内容4',
    '这是放大的内容5',
    '这是放大的内容6',
    '这是放大的内容7',
    '这是放大的内容8',
    '这是放大的内容9',
    '这是放大的内容10'
];
 // 存储初始内容
 const initialContents = [];
// 块放大效果的逻辑
const fancyDivs = document.querySelectorAll('.fancydiv');
let eventsBound1 = false; 
document.addEventListener("DOMContentLoaded", function () {
    
    let currentUserId = null; // 当前登录用户的 ID

    // 获取当前登录用户信息
    fetch('/is_logged_in')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                currentUserId = data.user_id;
            }

            // 加载资源数据
            return fetch('/get_resources');
        })
        .then(response => response.json())
        .then(data => {
            // 随机打乱数据顺序
            const shuffledData = data.sort(() => Math.random() - 0.5);
            console.log(shuffledData);
            const mainContent = document.querySelector('.main-content');
            mainContent.innerHTML = ''; // 清空内容
            const maxDivs = 10; // 最大的 fancydiv 数量
            // 创建和填充 fancydivs
            for (let i = 0; i < maxDivs; i++) {
                const div = document.createElement('div');
                div.classList.add('fancydiv');
                
                div.id = `fancydiv${i + 1}`; // 生成唯一 ID
                if (i < shuffledData.length) {
                    const post = shuffledData[i];
                    const contentHTML = `
                        <img src="${post.image_path}" alt="封面图" class="fancy-image">
                        <div class="fancy-info">
                            <a class="user-avatar-link" data-user-id="${post.user_id}">
                                <img src="${post.avatar}" alt="用户头像" class="fancy-avatar">
                            </a>
                            <p class="fancy-author">发布人: ${post.author}</p>
                            ${currentUserId !== post.user_id 
                                ? `<button class="follow-button" data-user-id="${post.user_id}">${post.is_following ? '取消关注' : '关注'}</button>` 
                                : ''
                            }
                            <button class="like-button" data-post-id="${post.id}">${post.is_liked ? '取消点赞' : '点赞'}</button>
                            <p class="fancy-timestamp">发布时间: ${new Date(post.timestamp).toLocaleString()}</p>
                            <p class="fancy-title">内容: ${post.content}</p>
                            <div class="comment-section">
                            <textarea class="comment-input" data-post-id="${post.id}" placeholder="输入评论..."></textarea>
                            <button class="submit-comment" data-post-id="${post.id}">提交评论</button>
                            <!-- 动态评论列表 -->
                            <div class="comment-list" id="comment-list-${post.id}" style="display: none;"></div>
                            </div>
                        </div>
                    `;
                    div.innerHTML = contentHTML;
                    
                    initialContents.push(contentHTML); // 存储初始内容
                } else {
                    div.innerHTML = `<span>暂无内容</span>`; // 空位时占位内容
                    initialContents.push(`<span>暂无内容</span>`); // 存储占位内容
                }
                mainContent.appendChild(div);
            }

            // 获取创建的所有 fancydiv 元素
            const fancyDivs = document.querySelectorAll('.fancydiv');

            // 设置点击事件
            fancyDivs.forEach((fancydiv, index) => {
                fancydiv.addEventListener('click', (event) => {
                    event.stopPropagation();
                    const isOpen = fancydiv.classList.contains('fullscreen'); // 判断当前状态
                    const postId = fancydiv.querySelector('.submit-comment') ? fancydiv.querySelector('.submit-comment').getAttribute('data-post-id') : null;
                    
                    fancyDivs.forEach(div => {
                        if (div !== fancydiv) {
                            div.style.display = 'none'; // 隐藏其他块
                            div.classList.remove('expand'); // 移除扩展类
                            div.classList.add('shrink'); // 添加缩小类
                            
                        } else {
                            div.classList.toggle('fullscreen'); // 切换全屏效果
                            console.log(div)
                            
                            if (!isOpen) 
                                return;
                        }
                        
                    });
                    
                    if (isOpen) {
                        fancydiv.classList.remove('expand'); // 移除扩展类
                        fancydiv.classList.add('shrink'); // 添加缩小类
                        fancydiv.innerHTML = initialContents[index]; // 恢复初始内容
                        fancyDivs.forEach(div => div.style.display = 'flex'); // 恢复显示其他块
                        fancydiv.scrollIntoView({ behavior: 'auto', block: 'start' }); // 跳转
                        loadComments(fancydiv, postId); 
                        if(postId){
                            rebindEvents(fancydiv); // 确保事件重新绑定
                        }
                        }
                        else {
                        fancydiv.classList.add('expand'); // 添加扩展类
                        fancydiv.classList.remove('shrink'); // 移除缩小类
                        loadComments(fancydiv, postId); 

                    }
                    
                });
            });
            if(eventsBound1==false){
                console.log("初始化");
            // 绑定头像点击事件
            bindAvatarClickEvents();

            // 绑定关注按钮点击事件
const fancydivElements = document.querySelectorAll('.fancydiv');
fancydivElements.forEach(fancydiv => {
    bindFollowButtonEvent(fancydiv); // 为每个 fancydiv 绑定关注按钮事件
});

// 绑定点赞按钮点击事件
fancydivElements.forEach(fancydiv => {
    bindLikeButtonEvent(fancydiv); // 为每个 fancydiv 绑定点赞按钮事件
});
             // 绑定评论按钮点击事件
             bindAllCommentButtons() ;
             //评论框防冒泡设计
            bindCommentInputEvents();
            eventsBound1=true;
            }
        })
        .catch(error => console.error('Error fetching posts:', error));
});
 // 重新绑定事件的函数
 function rebindEvents(fancydiv) {
    console.log(111);
        // 重新绑定头像点击事件
        bindAvatarClickEvents();

        // 重新绑定关注按钮点击事件
        bindFollowButtonEvent(fancydiv);

        // 重新绑定点赞按钮点击事件
        bindLikeButtonEvent(fancydiv);

        // 重新绑定评论按钮点击事件
        const commentButton = fancydiv.querySelector('.submit-comment');
        bindCommentButtonEvent(commentButton);

         // 评论框防冒泡设计
        const commentInputs = fancydiv.querySelectorAll('.comment-input');
        commentInputs.forEach(input => {
        input.addEventListener('click', function (event) {
            event.stopPropagation(); // 阻止事件冒泡
        });
        });

}
function bindCommentButtonEvent(button) {
    button.addEventListener('click', function (event) {
        event.stopPropagation(); // 阻止事件冒泡

        const postId = this.getAttribute('data-post-id');
        const commentInput = document.querySelector(`textarea.comment-input[data-post-id="${postId}"]`);
        const commentText = commentInput.value.trim();
        const fancydiv = this.closest('.fancydiv'); // 获取当前按钮所在的 fancydiv 元素

        if (commentText) {
            // 调用提交评论函数，传递 fancydiv 和 postId
            submitComment(fancydiv, postId, commentText);
        } else {
            alert('评论内容不能为空');
        }
    });
}
// 单独为所有评论按钮绑定事件
function bindAllCommentButtons() {
    const commentButtons = document.querySelectorAll('.submit-comment');
    commentButtons.forEach(button => {
        bindCommentButtonEvent(button);
    });
}
// 提交评论的函数
function submitComment(fancydiv, postId, commentText) {
    
    fetch('/submit_comment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            post_id: postId,
            content: commentText
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 评论提交成功后更新评论区域
            loadComments(fancydiv, postId);  // 重新加载评论
            alert('评论提交成功！');

            const commentInput = fancydiv.querySelector('.comment-input');
            if (commentInput) {
                commentInput.value = '';  // 清空评论输入框
            }
        } else {
            alert('评论提交失败，请稍后再试');
        }
    })
    .catch(error => {
        console.error('提交评论失败:', error);
        alert('评论提交失败，请稍后再试');
    });
}

// 绑定评论框点击事件，防止事件冒泡
function bindCommentInputEvents() {
    const commentInputs = document.querySelectorAll('.comment-input');
    commentInputs.forEach(input => {
        input.addEventListener('click', function (event) {
            console.log(111);
            event.stopPropagation(); // 阻止事件冒泡
        });
    });
}

// 加载评论的函数
function loadComments(fancydiv,postId) {
    const commentList = fancydiv.querySelector('.comment-list')
    if (!fancydiv.classList.contains('fullscreen')) {
        return; // 如果当前 fancydiv 没有处于放大状态，则不执行加载评论的逻辑
    }
    if (postId) {
        // 获取当前登录用户信息
        fetch('/is_logged_in')
            .then(response => response.json())
            .then(loginData => {
                const currentUserId = loginData.logged_in ? loginData.user_id : null;

                // 请求评论数据
                fetch(`/get_comments?post_id=${postId}`)
                    .then(response => response.json())
                    .then(data => {
                        commentList.innerHTML = ''; // 清空评论内容
                        data.comments.forEach(comment => {
                            // 检查评论是否由当前用户发布
                            const isCurrentUser = currentUserId && comment.user_id === currentUserId;
                            console.log(comment.user_id);
                            console.log(currentUserId);
                            const deleteButtonHTML = isCurrentUser 
                                ? `<button class="delete-comment-button" data-comment-id="${comment.id}">删除</button>` 
                                : '';

                            const commentHTML = `
                                <div class="comment">
                                    <p>
                                        <strong>${comment.username}</strong>: ${comment.content}
                                        ${deleteButtonHTML}
                                    </p>
                                </div>
                            `;
                            commentList.innerHTML += commentHTML;
                        });

                        // 绑定删除按钮事件
                        if (currentUserId) {
                            bindDeleteCommentEvents(commentList);
                        }
                        
                        // 显示评论列表
                        commentList.style.display = 'block';
                    })
                    .catch(error => {
                        console.error('加载评论时发生错误:', error);
                    });
            })
            .catch(error => {
                console.error('获取当前用户信息时发生错误:', error);
            });
    }

}
// 删除评论按钮绑定事件
function bindDeleteCommentEvents(commentList) {
    const deleteButtons = commentList.querySelectorAll('.delete-comment-button');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.stopPropagation(); // 阻止事件冒泡

            const commentId = this.getAttribute('data-comment-id');
            fetch(`/delete_comment/${commentId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({}) // 发送空对象即可
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 删除评论成功后，移除该评论元素
                    this.closest('.comment').remove();
                    alert('评论已删除');
                } else {
                    alert(data.message); // 显示错误信息
                }
            })
            .catch(error => {
                console.error('删除评论失败:', error);
                alert('删除评论失败，请稍后再试');
            });
        });
    });
}


function bindAvatarClickEvents() {
    const avatarLinks = document.querySelectorAll('.user-avatar-link');
    avatarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.stopPropagation();
            
            const userId = this.getAttribute('data-user-id');
            const targetUrl = `/user/${userId}`;
            console.log("点击头像，目标 URL:", targetUrl);

            fetch('/is_logged_in')
                .then(response => response.json())
                .then(data => {
                    if (!data.logged_in) {
                        event.preventDefault(); // 阻止默认跳转
                        console.log("用户未登录，跳转到登录页面");
                        window.location.href = '/login';
                    } else {
                        console.log("用户已登录，跳转到:", targetUrl);
                        window.location.href = targetUrl;
                    }
                })
                .catch(error => {
                    console.error('检查登录状态时发生错误:', error);
                    event.preventDefault();
                });
        });
    });
}
function updateAllPostsFollowStatus(userId, isFollowing) {
    const allFollowButtons = document.querySelectorAll('.follow-button');
    allFollowButtons.forEach(button => {
        const postUserId = button.getAttribute('data-user-id');
        if (postUserId === userId) {
            console.log(1);
            button.textContent = isFollowing ? '取消关注' : '关注';
        }
    });
}

function bindFollowButtonEvent(fancydiv) {
    const followButtons = fancydiv.querySelectorAll('.follow-button');
    followButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const userId = this.getAttribute('data-user-id');
            event.stopPropagation();

            fetch('/is_logged_in')
                .then(response => response.json())
                .then(data => {
                    if (!data.logged_in) {
                        console.log("用户未登录，跳转到登录页面");
                        window.location.href = '/login';
                        return;
                    }

                    // 向后端发送关注或取消关注请求
                    fetch('/toggle_follow', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ follower_id: data.user_id, followed_id: userId })
                    })
                        .then(response => response.json())
                        .then(result => {
                            if (result.success) {
                                // 更新当前按钮文本
                                this.textContent = this.textContent === '关注' ? '取消关注' : '关注';
                                console.log(`关注状态已更新为: ${this.textContent}`);

                                // 获取当前 fancydiv
                                if (fancydiv) {
                                    const index = [...fancydiv.parentNode.children].indexOf(fancydiv);
                                    const updatedHTML = fancydiv.innerHTML; // 获取更新后的内容
                                    initialContents[index] = updatedHTML; // 更新 initialContents
                                }

                                // 更新所有相关帖子的关注状态
                                console.log(userId);
                                updateAllPostsFollowStatus(userId, result.is_following);
                            } else {
                                console.error('更新关注状态失败:', result.message);
                            }
                        })
                        .catch(error => console.error('请求失败:', error));
                })
                .catch(error => console.error('检查登录状态时发生错误:', error));
        });
    });
}

function bindLikeButtonEvent(fancydiv) {
    const likeButtons = fancydiv.querySelectorAll('.like-button');
    likeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const postId = this.getAttribute('data-post-id');
            event.stopPropagation();
            console.log("点赞绑定成功");

            fetch('/is_logged_in')
                .then(response => response.json())
                .then(data => {
                    if (!data.logged_in) {
                        console.log("用户未登录，跳转到登录页面");
                        window.location.href = '/login';
                        return;
                    }

                    // 向后端发送点赞请求
                    fetch(`/like_post/${postId}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                    })
                        .then(response => {
                            console.log("点赞状态更新成功");

                            // 更新点赞按钮的状态或样式
                            console.log(this.textContent);
                            this.textContent = this.textContent === '点赞' ? '取消点赞' : '点赞';
                            console.log(this.textContent);

                            // 获取当前 fancydiv
                            if (fancydiv) {
                                const index = [...fancydiv.parentNode.children].indexOf(fancydiv);
                                const updatedHTML = fancydiv.innerHTML; // 获取更新后的内容
                                initialContents[index] = updatedHTML; // 更新 initialContents
                                console.log(fancydiv);
                            }
                        })
                        .catch(error => console.error('请求失败:', error));
                })
                .catch(error => console.error('检查登录状态时发生错误:', error));
        });
    });
}


function handlePageTransition(url) {
    document.body.classList.add('fade-out');

    setTimeout(function() {
        window.location.href = url;
    }, 500);
}

// 处理下拉菜单的显示与隐藏
function handleDropdownClick(button, url) {
    var dropdownContent = button.nextElementSibling;

    // 关闭其他打开的下拉菜单
    var openDropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < openDropdowns.length; i++) {
        if (openDropdowns[i] !== dropdownContent) {
            openDropdowns[i].classList.remove('show');
        }
    }

    // 切换当前下拉菜单的显示状态
    dropdownContent.classList.toggle('show');

    // 如果点击的是按钮而非下拉菜单项，则跳转
    var event = window.event; // 用于获取事件对象
    if (!event.target.closest('.dropdown-content')) {
        handlePageTransition(url); // 使用新的函数进行页面切换
    }
}

// 当点击文档其他地方时关闭所有下拉菜单
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

// 展示导航栏
function showNavbar() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.add('show'); // 显示导航栏
}

// 隐藏导航栏
function hideNavbar() {
    const navbar = document.querySelector('.navbar');
    navbar.classList.remove('show'); // 隐藏导航栏
}

// 处理鼠标悬停和离开的状态
document.querySelector('.show-navbar-btn').addEventListener('mouseenter', showNavbar);
document.querySelector('.show-navbar-btn').addEventListener('mouseleave', hideNavbar);
document.querySelector('.navbar').addEventListener('mouseenter', showNavbar);
document.querySelector('.navbar').addEventListener('mouseleave', hideNavbar);