import { createRoot } from 'react-dom/client';
import RelatedProblem from "./RelatedProblem"
import MyPage from "./MyPage"
import React from 'react';

function IfSubmitPage() {
    const currentPageURL = window.location.href;
    const desiredURLPattern = "https://www.acmicpc.net/status?from_mine=";
    return currentPageURL.startsWith(desiredURLPattern);
}

function IfMyPage() {
    const currentPageURL = window.location.href;
    const desiredURLPattern = "https://www.acmicpc.net/user/";
    return currentPageURL.startsWith(desiredURLPattern);
}    

if (IfSubmitPage()) {
    const appContainer = document.createElement('div');
    const targetElement = document.querySelector('body > div.wrapper > div.container.content > div.row > div.margin-bottom-30') as HTMLElement;
    if (targetElement) {
        const styles = {
            backgroundColor: '#F5F5F5',
            width: '97.5%', // 원하는 너비로 설정
            height: '29px', // 원하는 높이로 설정
            position: 'relative', // 위치 지정을 상대적으로 설정
            left: '13px', // 원하는 오른쪽 이동 거리로 설정
            top: '15px' // 원하는 아래로 이동 거리로 설정
        };
        Object.assign(targetElement.style, styles);
    }
    targetElement?.appendChild(appContainer);
    const root = createRoot(appContainer);
    root.render(<RelatedProblem />)
}

if (IfMyPage()) {
    const targetSelector = "body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(1) > div.panel-body";
    const targetElement = document.querySelector(targetSelector);
    
    const parentElement = targetElement.parentElement;
    
    // 새로운 divElement를 생성하여 첫 번째 root를 생성합니다.
    const divElement1 = document.createElement("div");
    parentElement.appendChild(divElement1);
    const root1 = createRoot(divElement1);
    //root1.render(<ProsCons />);
    
    // 새로운 divElement를 생성하여 두 번째 root를 생성합니다.
    const divElement2 = document.createElement("div");
    parentElement.appendChild(divElement2);
    const root2 = createRoot(divElement2);
    root2.render(<MyPage />);
}