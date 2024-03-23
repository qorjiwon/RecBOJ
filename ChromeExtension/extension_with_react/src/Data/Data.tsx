import axios from 'axios'

export const getData = async (
    url: string,
    rotate: number,
    filterTier: string
): Promise<ResponseData|null> => {
    try {
      // https://recproblem.site
      const response = await axios.post(
          'http://127.0.0.1:8000/mypage/problems',
          {
              url,
              div: rotate,
              filter: filterTier,
          },
          {
              headers: {
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response) {
            return response.data;
        }
        return null
    }
    catch (error) {
      console.error('에러 발생:', error);
      return null
    }
}

export type MyPageRequest = {
    url: string;
    div: number;
    filter: string;
}  

export type Problem = {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
    tags: string[];
}

export type Explaination = {
    problemID: string;
    titleKo: string;
    level: string;
    averageTries: number;
}

export type Tag = {
    tag_name: string;
    problems: string[];
    explainations: Explaination[];
    weak_pcr: number;
}

export type WeakTagProblems = {
    [key: string]: Tag;
}

export type ForgottenTagProblems = {
    [key: string]: {
        tag: string;
        forgottenPercent: number;
        problem: Problem;
    };
}

export type SimilarityBasedProblems = {
    problem1: Problem;
    problem2: Problem;
    problem3: Problem;
}

export type ResponseData = {
    user_id: string;
    weak_tag_problems: WeakTagProblems;
    forgotten_tag_problems: ForgottenTagProblems;
    similarity_based_problems: SimilarityBasedProblems;
}