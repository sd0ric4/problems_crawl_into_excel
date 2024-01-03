// ==UserScript==
// @name         题目爬取脚本
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  爬取题目和答案
// @author       sd0ric4
// @match      	 *://*.chaoxing.com/*
// @grant        none
// ==/UserScript==

(function () {
    'use strict';
    const questionContainer = document.querySelector('.clearfix');
    function getJson() {

        // 获取章节名称
        const chapter = document.querySelector('.ceyan_name h3').innerText.trim().replace(/\n/g, '');

        // 获取所有题目的容器
        const questions = document.querySelectorAll('.TiMu');

        // 用于存储所有题目数据的数组
        let data = [];

        questions.forEach((question) => {
            // 获取题目类型
            const type = question.querySelector('.newZy_TItle').innerText.trim().replace(/\n/g, '').replace(/【|】/g, '');

            // 获取题干
            const title = question.querySelector('.font-cxsecret').innerText.trim().replace(/\n/g, '');

            // 获取选项
            let options = [];
            const optionsList = question.querySelectorAll('.Zy_ulTop li');
            if (type == "单选题" || type == "多选题") {
                optionsList.forEach((option) => {
                    const optionText = option.innerText.trim().replace(/\n/g, '');
                    //console.log(optionText);
                    const optionKey = optionText.charAt(0);
                    const optionValue = optionText.substring(2);
                    options[optionKey] = optionValue;
                    //console.log(options);
                    options.push({ [optionKey]: optionValue });
                });
            }
            else if (type == "判断题") {
                //判断题 固定 把选项设置成A. 对 B. 错
                options.push({ "A": "对" });
                options.push({ "B": "错" });

            }



            // 获取正确答案,并将判断题的对错转换成A或B
            let correctAnswer = any
            if (type == "填空题") {
                const blankAnswerElement = question.querySelector('.correctAnswer.marTop16');
                correctAnswer = blankAnswerElement.innerText.trim().split('：')[1];
            }
            else {
                correctAnswer = question.querySelector('.correctAnswer .answerCon').innerText.trim().replace(/\n/g, '');
            }
            // 将题目数据添加到数组
            data.push({
                chapter,
                type,
                title,
                options,
                correctAnswer
            });
        });

        // 输出JSON格式的数据
        console.log(JSON.stringify(data));
        return data;
    }

    function exportJson() {
        const chapter = document.querySelector('.ceyan_name h3').innerText.trim().replace(/\n/g, '');
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'export-button-container';

        const button = document.createElement('a');
        button.className = 'jb_btn_bg';
        button.innerText = '导出JSON';
        button.href = '#';
        button.addEventListener('click', () => {
            const jsonData = JSON.stringify(getJson());
            const blob = new Blob([jsonData], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = chapter + '.json';
            a.click();
            URL.revokeObjectURL(url);
        });

        buttonContainer.appendChild(button);

        const ansbtnBox = document.querySelector('.ansbtnBox');
        ansbtnBox.appendChild(buttonContainer);
    }


    exportJson();





})();
