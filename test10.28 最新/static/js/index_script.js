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
const fancyDivs = document.querySelectorAll('.fancydiv');



document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_resources')  // 调用 API
        .then(response => response.json())
        .then(data => {
            // 随机打乱数据顺序
            const shuffledData = data.sort(() => Math.random() - 0.5);

            const mainContent = document.querySelector('.main-content');
            mainContent.innerHTML = ''; // 清空内容
            const maxDivs = 10; // 最大的 fancydiv 数量

            // 存储初始内容
            const initialContents = [];

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
                            <h3 class="fancy-title">内容: ${post.content}</h3>
                            <p class="fancy-author">发布人: ${post.author}</p>
                            <p class="fancy-timestamp">发布时间: ${new Date(post.timestamp).toLocaleString()}</p>
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
                fancydiv.addEventListener('click', () => {
                    // 检查是否有其他块在全屏
                    const isOpen = fancydiv.classList.contains('fullscreen'); // 判断当前状态

                    fancyDivs.forEach(div => {
                        if (div !== fancydiv) {
                            // 如果当前块不是被点击的块，收起其他块
                            div.style.display = 'none'; // 隐藏其他块
                            div.classList.remove('expand'); // 移除扩展类
                            div.classList.add('shrink'); // 添加缩小类
                        } else {
                            div.classList.toggle('fullscreen'); // 切换全屏效果
                            if (!isOpen) {
                                // 如果当前块是打开状态，则不进行滚动
                                return;
                            }
                        }
                    });

                    // 根据当前状态切换文本内容和扩展类
                    if (isOpen) {
                        fancydiv.classList.remove('expand'); // 移除扩展类
                        fancydiv.classList.add('shrink'); // 添加缩小类
                        fancydiv.innerHTML = initialContents[index]; // 恢复初始内容
                        fancyDivs.forEach(div => {
                            div.style.display = 'flex'; // 恢复显示其他块
                        });

                        // 直接滚动到当前块位置
                        fancydiv.scrollIntoView({ behavior: 'auto', block: 'start' }); // 直接跳转
                    } else {
                        fancydiv.classList.add('expand'); // 添加扩展类
                        fancydiv.classList.remove('shrink'); // 移除缩小类
                        // 不需要改变内容，保持初始内容
                    }
                });
            });
        })
        .catch(error => console.error('Error fetching posts:', error));
});

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



