import React, { useState, useEffect} from 'react';
import "./MyPage.css";
import ReactTooltip from 'react-tooltip';
import { CSSTransition } from 'react-transition-group';
import Tag from './Component/Tag';
import { ResponseData, getData } from '../../Data/Data';

const PROBLEM_SIZE = 3

function MyPage() { // 사용자 상세 페이지 렌더링
      const [problems, setProblems] = useState<ResponseData|null>(null);
      const [currentPage, setCurrentPage] = useState(-1); // 취약 유형 기반, 푼 지 오래된 문제, 실력 기반
      const [selectedField_weak, setSelectedField_weak] = useState(0); // 취약 유형
      const [rotate, setRotate] = useState(0); // 새로고침.. python에서 배열에 저장해놓고 가져오도록 구현함
      const [isOptionsVisible, setOptionsVisible] = useState(false);
      const [filterTier, setFilter] = useState('None');

      const url= window.location.href;

      useEffect(() => {
          (async () => {
            try {
              const response = await getData(url, PROBLEM_SIZE, rotate, filterTier)
              if (response) {
                setProblems(response);
                setCurrentPage(0);
              }
              }
              catch (error) {
                console.error('에러 발생:', error);
              }
          })();
      }, [rotate]);
      
    useEffect(() => {
        ReactTooltip.rebuild();
    }, []);


    const toggleOptions = () => {
        setOptionsVisible(!isOptionsVisible);
      };
  
     const handleFilter = (tier) => {
        setFilter(tier);
        toggleOptions();
     }

    // 클릭 이벤트 핸들러
    const contentClick = (url) => {
        // 동적으로 생성된 URL을 사용하려면 여기에서 로직을 추가
        const dynamicURL = url; // 동적으로 생성된 URL

        // 지정된 URL로 이동
        window.location.href = dynamicURL;
    };

    const TypeOfRecommendation = ['취약 유형 기반 추천', '실력 기반 추천', '푼 지 오래된 문제 추천']
    const Tiers = ['Random', 'Silver', 'Gold', 'Platinum', 'Diamond']

    return (
        <div className="RecBOJ">
            { problems &&
                <header className="HeaderBar">
                    {
                        TypeOfRecommendation.map((text, index) => (
                            <button
                                key={index}
                                className={`manu ${currentPage === index ? 'active' : ''}`}
                                onClick={() => setCurrentPage((currentPage) => (currentPage === index ? -1 : index))}
                            >
                                {text}
                            </button>
                        ))
                    }
                </header>
            }
            <div className="RecommendBox">
                {
                    !problems && <div>
                        <img src='https://velog.velcdn.com/images/qorjiwon/post/0de07a4d-690f-4f6a-b319-fceb8058e093/image.gif'/>
                    </div>
                }
                { currentPage === 0 && ( // 취약 유형 기반
                    <>
                        <div className='WeekTags'>
                            {
                                problems.weak_tag_problems.map((tag, index) => {
                                    return (
                                        <button key={tag.tag_name} className='WeekTagBtn' onClick={() => setSelectedField_weak(index)}>
                                            {tag.tag_name}
                                        </button>
                                    )
                                })
                            }
                        </div>

                        <p className='Message'>
                            {`${problems.weak_tag_problems[selectedField_weak].weak_pcr}%만큼 약한 분야에요.`}
                        </p>
                    
                        <div className={'OtherProblems'}>
                            <button className='ReloadingM' onClick={() => setRotate((rotate) => rotate + 1)}/>
                            <div className="OptionsContainer">
                                <button className="ToggleOptions" onClick={toggleOptions} > {'난이도 필터'} </button>
                                <CSSTransition
                                    in={isOptionsVisible}
                                    timeout={250}
                                    classNames="options"
                                    unmountOnExit
                                >
                                    <div className="Tiers">
                                        {
                                            Tiers.map((tier) => 
                                                <button onClick={() => 
                                                    {
                                                        handleFilter(tier);
                                                        setRotate(0)
                                                    }}>
                                                    {tier}
                                                </button>)
                                        }
                                    </div>
                                </CSSTransition>
                            </div>
                        </div>
                        <div className="Problems" >
                            {
                                problems.weak_tag_problems[selectedField_weak].explainations ?.map((problem, index) => {
                                    return  (
                                        <a
                                            className='ProblemCard'
                                            data-tip={`${problem['problemID']}번 풀러 가기`}
                                            onClick={() => contentClick(`https://www.acmicpc.net/problem/${problem['problemID']}`)}
                                        >
                                            <p className={'ProblemName'}>{problem['titleKo']}</p>
                                            <p >난이도: {problem['level']}</p>
                                            <p>평균 시도 횟수: {problem['averageTries']}</p>
                                        </a>
                                    )
                                })
                            }
                        </div>
                        
                        <div className={'ServiceView'}>
                            <span data-tip = {`취약 유형은 ${problems.user_id}님의 해당 유형의 정답률, 푼 문제 수 등을 고려하여 산출돼요.`}>{'취약 유형이란?'}</span>
                            <ReactTooltip place="left" type="dark" effect="solid"/>
                        </div>
                    </>
                )}
                { currentPage === 1 && (
                    <>
                        <p className='Message'>
                            {'이런 문제는 어떤가요?'}
                        </p>
                        <p><b>{problems.user_id}</b>{'님과 비슷한 실력의 유저들이 많이 푼 문제들을 가져왔어요!'}</p>
                        
                        <div className={'OtherProblems'}>
                            <button className='ReloadingM' onClick={() => setRotate((rotate) => rotate + 1)}/>
                            <div className="OptionsContainer">
                                <button className="ToggleOptions" onClick={toggleOptions} > {'난이도 필터'} </button>
                                <CSSTransition
                                    in={isOptionsVisible}
                                    timeout={250}
                                    classNames="options"
                                    unmountOnExit
                                >
                                    <div className="Tiers">
                                        {
                                            Tiers.map((tier) => 
                                                <button onClick={() => 
                                                    {
                                                        handleFilter(tier);
                                                        setRotate(0)
                                                    }}>
                                                    {tier}
                                                </button>)
                                        }
                                    </div>
                                </CSSTransition>
                            </div>
                        </div>
                        <div className='Problems'>
                            {
                                problems.similarity_based_problems.map((problem) => {
                                    return (
                                        <a className='ProblemCard'
                                            data-tip = {`난이도: ${problem.level}, 분류: ${problem.tags}`}
                                            href = {`https://www.acmicpc.net/problem/${problem.problemID}`}
                                        >
                                            <p className={'ProblemName'}>{problem.titleKo}</p>
                                            <p>난이도: {problem.level}</p>
                                            <p>평균 시도 횟수: {problem.averageTries}</p>
                                            <p>분류: {problem.tags}</p>
                                        </a>
                                    )
                                })
                            }
                        </div>
                    </>
                )}
                { currentPage === 2 && (
                    <>
                        <div className={'BlurredSection'}>
                            <p className='Message'>
                                {'해당 분류의 문제를 푼 지 오래됐어요.'}
                            </p>
                            <p style={{textAlign: 'center', marginBottom: '0px', color: '#5f6368'}}>{'나중엔 더 기억나지 않을 거예요!'}</p>
                            
                            <div className={'OtherProblems'}>
                                <button className='ReloadingM' onClick={() => setRotate((rotate) => rotate + 1)}/>
                                <div className="OptionsContainer">
                                    <button className="ToggleOptions" onClick={toggleOptions} > {'난이도 필터'} </button>
                                    <CSSTransition
                                        in={isOptionsVisible}
                                        timeout={250}
                                        classNames="options"
                                        unmountOnExit
                                    >
                                        <div className="Tiers">
                                            {
                                                Tiers.map((tier) => 
                                                    <button onClick={() => 
                                                        {
                                                            handleFilter(tier);
                                                            setRotate(0)
                                                        }}>
                                                        {tier}
                                                    </button>)
                                            }
                                        </div>
                                    </CSSTransition>
                                </div>
                            </div>

                            <div className='Problems'>
                                {
                                    problems.forgotten_tag_problems.map((problemInfo) => {
                                        return (
                                            <a 
                                                className='ProblemCard'
                                                data-tip={`난이도: ${problemInfo.problem.level}, 분류: ${problemInfo.tag}`}
                                                onClick={() => contentClick(`https://www.acmicpc.net/problem/${problemInfo.problem.problemID}`)}
                                            >
                                                <p className={'ProblemName'}>{problemInfo.problem.titleKo}</p>
                                                {/* <p >난이도: {problemInfo.problem.level}</p> */}
                                                <p>{'현재 '}<b>{problemInfo.tag}</b>{'내용을 '}<b>{problemInfo.forgottenPercent}</b>{' 기억하고 있어요.'}</p>
                                                {/* <p>평균 시도 횟수: {problem['averageTries']}</p> */}
                                            </a>
                                        )
                                    })
                                }
                            </div>
                                
                            <div className={'ServiceView'}>
                                <a data-tip = {`해당 문제들은 독일의 심리학자 헤르만 에빙하우스의 망각곡선에 기반하여 ${problems.user_id}님이 오래 동안 풀지 않은 유형의 문제를 추천해 드리고 있어요.`}
                                    href='https://ko.wikipedia.org/wiki/%EB%A7%9D%EA%B0%81_%EA%B3%A1%EC%84%A0'
                                >
                                    {'에빙하우스의 망각곡선'}</a>
                                <ReactTooltip place="left" type="dark" effect="solid"/>
                            </div>
                        </div>
                        <div className={'Notice'}>
                            <div className={'Promise'}>{'곧 만나요!'}</div>
                            <span>{'해당 서비스를 열심히 제작하고 있습니다. 조금만 기다려 주세요!'}</span>
                        </div>
                    </>
                )}
        </div>
        </div>
    );
}
  
export default MyPage;