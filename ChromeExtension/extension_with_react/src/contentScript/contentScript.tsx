import { createRoot } from 'react-dom/client';
import React, { useState, useEffect } from 'react';

function shouldInsertCode() {
    const currentPageURL = window.location.href;
    const desiredURLPattern = "https://www.acmicpc.net/status?from_mine=";
    return currentPageURL.startsWith(desiredURLPattern);
}

interface ProblemsType {
    problem_equal: string;
    problem_low: string;
    problem_high: string;
}

function App() {
    const [problems, setProblems] = useState<ProblemsType | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8080/send_url', {
                    method: 'POST',
                    body: JSON.stringify({ url: window.location.href }),
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
        for (const key in problems) {
            const problemNumber = problems[key as keyof ProblemsType];
            const url = `https://www.acmicpc.net/problem/${problemNumber}`;
            urls[key as keyof ProblemsType] = url;
            problem_ids[key as keyof ProblemsType] = problemNumber;
        }
    }

    console.log("URL1 =", urls.problem_equal);
    console.log("URL2 =", urls.problem_low);
    console.log("URL3 =", urls.problem_high);

    console.log(urls);

    if (!problems) {
        return null;
    }

    return (
        <div>
            &nbsp; 추천 문제 (하): <a href={urls.problem_low}>{problem_ids.problem_low}</a> &nbsp;
            &nbsp; 추천 문제 (중): <a href={urls.problem_equal}>{problem_ids.problem_equal}</a> &nbsp;
            &nbsp; 추천 문제 (상):  <a href={urls.problem_high}>{problem_ids.problem_high}</a> &nbsp;
        </div>
    );
}

if (shouldInsertCode()) {
    const appContainer = document.createElement('div');
    const targetElement = document.querySelector('body > div.wrapper > div.container.content > div.row > div.margin-bottom-30') as HTMLElement;
    if (targetElement) {
        targetElement.style.backgroundColor = '#F5F5F5'; 
    }
    targetElement?.appendChild(appContainer);
    const root = createRoot(appContainer);
    root.render(<App />);
}
