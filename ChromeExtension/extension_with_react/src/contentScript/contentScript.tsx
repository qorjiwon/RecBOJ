import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';
import "./contentScript.css";


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
    const [currentPage, setCurrentPage] = useState(0);
    const [active, setActive] = useState(null);

    const handleClick = (index) => {
        // 현재 클릭한 버튼이 이미 활성 상태라면 비활성 상태로, 그렇지 않다면 활성 상태로 설정
        console.log(currentPage, index);
        setCurrentPage((currentPage) => (currentPage === index ? 0 : index));
        setActive((active) => (active === index ? null : index));
    };

    return (
        <div className="style">
            <div style = {{flexDirection: 'column', display: 'inline-block', borderBottom: '1px solid #ddd'}}>
                <button
                    className={`manu ${active === 1 ? 'active' : ''}`}
                    onClick={() => handleClick(1)}
                >
                    취약 유형 기반 추천
                </button>
                <button
                    className={`manu ${active === 2 ? 'active' : ''}`}
                    onClick={() => handleClick(2)}
                >
                    푼 지 오래된 문제 추천
                </button>
                <button
                    className={`manu ${active === 3 ? 'active' : ''}`}
                    onClick={() => handleClick(3)}
                >
                    유사도 기반 추천
                </button>
            </div>
            <div>
                <div>
                    {currentPage === 1 && (
                    <>
                        <div style={{fontSize: '24px', fontFamily: 'Arial, sans-serif', margin: 'auto', textAlign: 'center', marginTop: '13px', color: '#6D7856'}}>
                            이런 문제는 어떤가요?
                        </div>
                        <div className='divStyle'>
                            <div className='Box' id = 'Box1'>
                                <div className = 'pBox' id = "Problem1">
                                    추천 문제 1번
                                </div>
                                <div className = 'eBox' id = "explanation1">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                            <div className='Box' id = 'Box2'>
                                <div className = 'pBox' id = "Problem2">
                                    추천 문제 2번
                                </div>
                                <div className = 'eBox' id = "explanation2">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                            <div className='Box' id = 'Box3'>
                                <div className = 'pBox' id = "Problem3">
                                    추천 문제 3번
                                </div>
                                <div className = 'eBox' id = "explanation3">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                        </div>
                        </>
                    )}
                    {currentPage === 2 && (
                        <>
                        <div style={{fontSize: '24px', fontFamily: 'Arial, sans-serif', margin: 'auto', textAlign: 'center', marginTop: '13px', color: '#6D7856'}}>
                            이런 문제는 어떤가요?
                        </div>
                        <div className='divStyle'>
                            <div className='Box' id = 'Box1'>
                                <div className = 'pBox' id = "Problem1">
                                    추천 문제 1번
                                </div>
                                <div className = 'eBox' id = "explanation1">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                            <div className='Box' id = 'Box2'>
                                <div className = 'pBox' id = "Problem2">
                                    추천 문제 2번
                                </div>
                                <div className = 'eBox' id = "explanation2">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                            <div className='Box' id = 'Box3'>
                                <div className = 'pBox' id = "Problem3">
                                    추천 문제 3번
                                </div>
                                <div className = 'eBox' id = "explanation3">
                                    추천 이유 등 메세지
                                </div>
                            </div>
                        </div>
                        </>
                    )}
                    {currentPage === 3 && (
                        <>
                        <div style={{fontSize: '24px', fontFamily: 'Arial, sans-serif', margin: 'auto', textAlign: 'center', marginTop: '13px', color: '#6D7856'}}>
                                이런 문제는 어떤가요?
                            </div>
                            <div className='divStyle'>
                                <div className='Box' id = 'Box1'>
                                    <div className = 'pBox' id = "Problem1">
                                        추천 문제 1번
                                    </div>
                                    <div className = 'eBox' id = "explanation1">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                                <div className='Box' id = 'Box2'>
                                    <div className = 'pBox' id = "Problem2">
                                        추천 문제 2번
                                    </div>
                                    <div className = 'eBox' id = "explanation2">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                                <div className='Box' id = 'Box3'>
                                    <div className = 'pBox' id = "Problem3">
                                        추천 문제 3번
                                    </div>
                                    <div className = 'eBox' id = "explanation3">
                                        추천 이유 등 메세지
                                    </div>
                                </div>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
}

interface tagsType {
    strong0: string;
    strong1: string;
    strong2: string;
    weak0: string;
    weak1: string;
    weak2: string;
}

const problems = {
    dp: ['문제 1', '문제 2', '문제 3'],
    graph: ['문제 4', '문제 5', '문제 6'],
    string: ['문제 7', '문제 8', '문제 9'],
    dac: ['문제 10', '문제 11', '문제 12'],
    ds : ['문제 13', '문제 14', '문제 15'],
    greedy: ['문제 16', '문제 17', '문제 18']
};

function ProsCons() {
    const [tags, setTags] = useState<tagsType | null>(null);
    const [selectedField, setSelectedField] = useState<string | null>(null);
    const [selectedButton, setSelectedButton] = useState<string | null>(null);

    const handleClick = (field: string) => {
        if (selectedField === field) {
            setSelectedField(null);
            setSelectedButton(null);
        } else {
            setSelectedField(field);
            setSelectedButton(field);
        }
    };

    useEffect(() => {
       
        const fetchTags = async () => {
        
                const response = await fetch('http://127.0.0.1:8080/tags', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href}),
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (!response.ok) {
                    throw new Error('서버 응답이 실패했습니다.');
                }
                const data = await response.json();
                let tagsData;
                try {
                    tagsData = JSON.parse(data.message);
                } catch (error) {
                    tagsData = data.message;
                }

                setTags(tagsData);
        };

        fetchTags();
    }, []);

    const buttonStyle = {
        border: '1px solid white',
        background: 'white',
        color: 'black',
        padding: '5px 10px',
        cursor: 'pointer',
        transition: 'background-color 0.3s, color 0.3s, font-size 0.3s'
    };
    return (
        <div style={{ display: 'flex', flexDirection: 'column', padding: '10px', margin: '5px' }}>
        <div style={{ border: '0.7px solid black', padding: '10px', marginBottom: '10px'}}>
            <b>강점 분야:</b>
            <button style={{ ...buttonStyle, background: selectedButton === 'dp' ? '#ecf0f1' : 'white', marginLeft: '1%', marginRight: '5%' }} onClick={() => handleClick('dp')}>DP</button>
            <button style={{ ...buttonStyle, background: selectedButton === 'graph' ? '#ecf0f1' : 'white', marginRight: '5%' }} onClick={() => handleClick('graph')}>Graphs</button>
            <button style={{ ...buttonStyle, background: selectedButton === 'greedy' ? '#ecf0f1' : 'white', marginRight: '5%' }} onClick={() => handleClick('greedy')}>Greedy</button>
        </div>
        <div style={{ border: '0.7px solid black', padding: '10px', marginBottom: '10px'}}>
            <b>약점 분야:</b>
            <button style={{ ...buttonStyle, background: selectedButton === 'string' ? '#ecf0f1' : 'white', marginLeft: '1%', marginRight: '5%' }} onClick={() => handleClick('string')}>String</button>
            <button style={{ ...buttonStyle, background: selectedButton === 'dac' ? '#ecf0f1' : 'white', marginRight: '5%' }} onClick={() => handleClick('dac')}>Divide and Conquer</button>
            <button style={{ ...buttonStyle, background: selectedButton === 'ds' ? '#ecf0f1' : 'white', marginRight: '5%' }} onClick={() => handleClick('ds')}>Data Structure</button>
        </div>
            {selectedField && (
                <div>
                    <h2>{selectedField} 관련 문제</h2>
                    <ul>
                        {problems[selectedField].map((problem, index) => (
                            <li key={index}>
                                <a href={`/${selectedField}/${problem}`}>{problem}</a>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

if (IfMyPage()) {
    const targetSelector = "body > div.wrapper > div.container.content > div.row > div:nth-child(2) > div > div.col-md-9 > div:nth-child(1) > div.panel-body";
    const targetElement = document.querySelector(targetSelector);
    
    const parentElement = targetElement.parentElement;
    
    // 새로운 divElement를 생성하여 첫 번째 root를 생성합니다.
    const divElement1 = document.createElement("div");
    parentElement.appendChild(divElement1);
    const root1 = createRoot(divElement1);
    root1.render(<ProsCons />);
    
    // 새로운 divElement를 생성하여 두 번째 root를 생성합니다.
    const divElement2 = document.createElement("div");
    parentElement.appendChild(divElement2);
    const root2 = createRoot(divElement2);
    root2.render(<MyPage />);
}