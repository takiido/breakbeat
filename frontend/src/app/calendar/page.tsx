"use client";

import { useState, useEffect } from "react";
import styles from "./styles.module.scss";

const weekdays = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
];

const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
];

function getDaysInMonth(year: number, month: number): number {
    return new Date(year, month + 1, 0).getDate();
}

function getYears(range: number = 10): number[] {
    const current: number = new Date().getFullYear();
    const years: number[] = [];

    for (let i: number = current - range; i <= current + range; ++i) {
        years.push(i);
    }

    return years;
}

function getMonBasedDayIndex(date: Date): number {
    return (date.getDay() + 6) % 7;
}

export default function Calendar() {

  const [days, setDays] = useState(0);
  const [month, setMonth] = useState(new Date().getMonth());
  const [year, setYear] = useState(new Date().getFullYear());
  const [weekday, setWeekday] = useState();

  const years = getYears();

  const totalCells = weekday + days;

  const cells = Array.from({length: totalCells}, (_, i) => {
      const dayNumber = i - weekday + 1;

      if (i < weekday) {
          return <div key={i} className={styles.day}></div>
      }

      return <div key={i} className={styles.day}>{dayNumber}</div>
  });

  useEffect(() => {
      setDays(getDaysInMonth(year, month));

      const firstDay = new Date(year, month, 1);
      setWeekday(getMonBasedDayIndex(firstDay));
  }, [month, year])

  return (
    <div>
      <select value={month} onChange={(e) => setMonth(Number(e.target.value))}>
        {months.map((m, i) => (
          <option key={m} value={i}>
            {m}
          </option>
        ))}
      </select>
      <select value={year} onChange={(e) => setYear(Number(e.target.value))}>
        {years.map((y) => (
          <option key={y} value={y}>
            {y}
          </option>
        ))}
      </select>

      <div className={styles.calendar}>
      {weekdays.map((wd) => (
          <div key={wd} className={styles.calendar_header}>
              {wd}
          </div>
      ))}
      {cells}
      </div>
    </div>
  );
}
