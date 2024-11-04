export const calculatePercent = (base: number | string, rate: number | string): string => {
  const baseValue = parseFloat(base.toString());
  const rateValue = parseFloat(rate.toString());

  if (isNaN(baseValue) || isNaN(rateValue)) {
    return '숫자를 입력해주세요';
  }

  const result = Math.floor(baseValue * (rateValue / 100)).toLocaleString('ko-KR');
  return `(변환 금액: ${result}원)`;
};
