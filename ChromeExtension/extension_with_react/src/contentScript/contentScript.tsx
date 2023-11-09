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
        borderRadius: '5px',
    };

    const divStyle = {
    border: '1px solid #ccc',
    padding: '10px',
    backgroundColor: 'rgb(207, 242, 135)',
    margin: '10px',
    width: '250px',
    };

    const Flexbox = {
        flexDirection: 'column' as 'column',
        display: 'inline-block', // Flexbox 레이아웃을 활용
        
    }

    const pieChartData = [
        { label: 'Bronze5', value: 10 },
        { label: 'Bronze4', value: 10 },
        { label: 'Bronze3', value: 10 },
        { label: 'Bronze2', value: 10 },
        { label: 'Bronze1', value: 10 },
        { label: 'Silver5', value: 10 },
        { label: 'Silver4', value: 10 },
        { label: 'Silver3', value: 10 },
        { label: 'Silver2', value: 10 },
        { label: 'Silver1', value: 10 },
        { label: 'Gold5', value: 10 },
        { label: 'Gold4', value: 10 },
        { label: 'Gold3', value: 10 },
        { label: 'Gold2', value: 10 },
        { label: 'Gold1', value: 10 },
        { label: 'Platinum5', value: 10 },
        { label: 'Platinum4', value: 10 },
        { label: 'Platinum3', value: 10 },
        { label: 'Platinum2', value: 10 },
        { label: 'Platinum1', value: 10 },
        { label: 'Diamond5', value: 10 },
        { label: 'Diamond4', value: 10 },
        { label: 'Diamond3', value: 10 },
        { label: 'Diamond2', value: 10 },
        { label: 'Diamond1', value: 10 }
    ];

    const pieChartColors = ['#9d4900', '#a54f00', '#ad5600', '#b55d0a', '#c67739', 
    '#38546e', '#3d5a74', '#435f7a', '#496580', '#4e6a86',
    '#d28500', '#df8f00', '#ec9a00', '#f9a518', '#ffb028',
    '#00C78B', '#00D497', '#27E2A4', '#3EF0B1', '#51FDBD',
    '#009EE5', '#00A9F0', '#00B4FC', '#2BBFFF', '#41CAFF'];

    return (
        <div style={style}>
            <div style={Flexbox}>
                <div style={divStyle}>
                    <p>취약 유형 기반 추천</p>
                </div>
                <div style={divStyle}>
                    <p>problem</p>
                </div>
                <div style={divStyle}>
                    <p>ㅁㅁ</p>
                </div>
            </div>
            <div style={Flexbox}>
                <div style={divStyle}>
                    <p>푼 지 오래된 문제 추천</p>
                </div>
                <div style={divStyle}>
                    <p>여기에 추가 내용이 있습니다.</p>
                </div>
                <div style={divStyle}>
                    <p>여기에 추가 내용이 있습니다.</p>
                </div>
            </div>
            <div style={Flexbox}>
                <div style={divStyle}>
                    <p>유사도 기반 추천</p>
                </div>
                <div style={divStyle}>
                    <p>여기에 추가 내용이 있습니다.</p>
                </div>
                <div style={divStyle}>
                    <p>여기에 추가 내용이 있습니다.</p>
                </div>
            </div>
            <div style={Flexbox}>
                <PieChart data={pieChartData} colors={pieChartColors} />
            </div>
        </div>
    );
}

interface PieChartProps {
    data: { label: string; value: number }[];
    colors: string[];
  }
  
  const PieChart: React.FC<PieChartProps> = ({ data, colors }) => {
    // 각 데이터 항목에 대한 각도 계산
    const total = data.reduce((acc, item) => acc + item.value, 0);
    let startAngle = 0;
  
    return (
      <svg width="250" height="250">
        {data.map((item, index) => {
          // 각 항목의 비율에 따라 각도 계산
          const angle = (item.value / total) * 360;
  
          // 현재 항목에 대한 색상 선택
          const color = colors[index % colors.length];
  
          // 원호 그리기
          const pathData = `
            M 125 125
            L ${125 + Math.cos((startAngle * Math.PI) / 180) * 100} ${125 + Math.sin((startAngle * Math.PI) / 180) * 100}
            A 100 100 0 ${angle > 180 ? 1 : 0} 1 ${125 + Math.cos(((startAngle + angle) * Math.PI) / 180) * 100} ${125 + Math.sin(((startAngle + angle) * Math.PI) / 180) * 100}
            Z
          `;
          // 다음 항목의 시작 각도 업데이트
          startAngle += angle;
  
          return <path key={index} d={pathData} fill={color} />;
        })}
      </svg>
    );
  };

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
