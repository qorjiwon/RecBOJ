import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';


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

interface ProblemsType {
    problem0: string;
    problem1: string;
    problem2: string;
    problem0_similarity: string;
    problem1_similarity: string;
    problem2_similarity: string;
    message;
}

function RelatedProblem() {
    const [problems, setProblems] = useState<ProblemsType | null>(null);

    useEffect(() => {
       
        const fetchData = async () => {
            // 모든 #solution-으로 시작하는 요소를 선택
            const elements = document.querySelectorAll("[id^='solution-'] > td.result > span.result-text");

            // 선택한 요소들의 텍스트를 가져옴
            const texts = Array.from(elements).map(element => element.textContent);
            
            // Flask에 URL 전송
            try {
                // 플라스크가 응답할 때까지 await
                const response = await fetch('http://127.0.0.1:8080/send_url', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href, submits: texts }),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('서버 응답이 실패했습니다.');
                }
                const data = await response.json();
                const problemsData = typeof data.message === 'string' ? JSON.parse(data.message) : data.message;
                setProblems(problemsData);
            }
            catch (error) {
                console.error('오류 발생: ' + error);
            }
        };

        fetchData();
    }, []);

    const urls: Record<string, string> = {};
    const problem_ids: Record<string, string> = {};

    if (problems) {
        for (let i = 0; i < 3; i++) { // problem0, problem1, problem2에 대해서만 반복
            const key = `problem${i}` as keyof ProblemsType;
            const problemNumber = problems[key];
            const url = `https://www.acmicpc.net/problem/${problemNumber}`;
            urls[key] = url;
            problem_ids[key] = problemNumber;
        }
    }

    console.log("URL_problem0 =", urls.problem0);
    console.log("URL_problem1 =", urls.problem1);
    console.log("URL_problem2 =", urls.problem2);

    console.log(urls);

    if (!problems) {
        return null;
    }
    return (
        <div id="myTooltip">
         <b>&nbsp; 연관 문제 1:</b> <a href={urls.problem0} style={{ fontWeight: 'bold',  marginRight: '10px'}}>{problem_ids.problem0}</a> &nbsp;
         <b>&nbsp; 연관 문제 2:</b> <a href={urls.problem1} style={{ fontWeight: 'bold',  marginRight: '10px'}}>{problem_ids.problem1}</a> &nbsp;
         <b>&nbsp; 연관 문제 3:</b> <a href={urls.problem2} style={{ fontWeight: 'bold',  marginRight: '10px'}}>{problem_ids.problem2}</a> &nbsp;
         <b>&nbsp; {problems.message}</b>
        </div>
    );
}

if (IfSubmitPage()) {
    const appContainer = document.createElement('div');
    const targetElement = document.querySelector('body > div.wrapper > div.container.content > div.row > div.margin-bottom-30') as HTMLElement;
    if (targetElement) {
        const styles = {
            backgroundColor: '#F5F5F5',
            width: '1143px', // 원하는 너비로 설정
            height: '27px', // 원하는 높이로 설정
            position: 'relative', // 위치 지정을 상대적으로 설정
            left: '13px', // 원하는 오른쪽 이동 거리로 설정
            display: 'flex', // Flexbox 레이아웃 사용
            alignItems: 'center', // 수직 가운데 정렬
            top: '15px' // 원하는 아래로 이동 거리로 설정
        };
        Object.assign(targetElement.style, styles);
    }
    targetElement?.appendChild(appContainer);
    const root = createRoot(appContainer);
    root.render(<RelatedProblem />)
}


function MyPage() {
    const style = {
        padding: '10px',
    };

    const divStyle = {
    padding: '10px',
    margin: '10px',
    width: '97%',
    height: '300px',
    border: '1px solid #ddd',
    borderRadius: '10px'
    };

    const manuBox = {
        flexDirection: 'column' as 'column',
        display: 'inline-block', // Flexbox 레이아웃을 활용
        borderBottom: '1px solid #ddd', // 선 추가
    }

    const [currentPage, setCurrentPage] = useState(0);

    const buttonStyle = {
        padding: '10px',
        margin: '10px',
        width: '250px',
        backgroundColor: '#FFFFFF',
        color: '#333',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        transition: 'background-color 0.3s, color 0.3s, font-size 0.3s', // 색 변화, 글자 굵기 및 크기 변화를 부드럽게 만들기 위한 트랜지션
        fontSize: '15px'
    }
    
    const activeStyle = {
        backgroundColor: '#E0E0E0',
        fontWeight: 'bold',
        fontSize: '15px'
    };    

    return (
        <div style={style}>
            <div style={manuBox}>
                <button
                    style={{ ...buttonStyle, ...(currentPage === 1 && activeStyle) }}
                    onClick={() => setCurrentPage(1)}
                >
                    취약 유형 기반 추천
                </button>
                <button
                    style={{ ...buttonStyle, ...(currentPage === 2 && activeStyle) }}
                    onClick={() => setCurrentPage(2)}
                >
                    푼 지 오래된 문제 추천
                </button>
                <button
                    style={{ ...buttonStyle, ...(currentPage === 3 && activeStyle) }}
                    onClick={() => setCurrentPage(3)}
                >
                    유사도 기반 추천
                </button>
            </div>
            <div>
                <div>
                    {currentPage === 1 && (
                        <div>
                            <div style={{ fontSize: '24px', fontFamily: 'Arial, sans-serif', margin: 'auto', textAlign: 'center' }}>
                                <h1>이런 문제는 어떤가요?</h1>
                            </div>
                            <div style = {divStyle}>
                                <p>ss</p>
                            </div>
                        </div>
                    )}
                    {currentPage === 2 && (
                        <>
                            <p>푼 지 오래된 문제 추천</p>
                            {/* 여기에 푼 지 오래된 문제 추천 내용 추가 */}
                        </>
                    )}
                    {currentPage === 3 && (
                        <>
                            <p>유사도 기반 추천</p>
                            {/* 여기에 유사도 기반 추천 내용 추가 */}
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

if (IfMyPage()) {

    // 삽입할 div 요소를 생성합니다.
    const divElement = document.createElement("div");

    const targetSelector = "body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(1) > div.panel-body";
    const targetElement = document.querySelector(targetSelector);

    // 선택한 요소의 부모 요소를 찾아서 그 아래에 div 요소를 삽입합니다.
    const parentElement = targetElement.parentElement;
    parentElement.appendChild(divElement);

    const root = createRoot(divElement);
    root.render(<MyPage />)
}
