import React, { useState, useRef, useEffect } from "react";
import { Line } from "react-chartjs-2";
import "chartjs-adapter-luxon";
import StreamingPlugin from "chartjs-plugin-streaming";

import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(
  StreamingPlugin,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const App = () => {
  const [items, setItems] = useState([]);

  const ws = useRef(null);
  const visible = useRef(null);

  var options = {
    plugins: {
      streaming: {
        duration: 30000,
      },
    },
    scales: {
      x: {
        type: "realtime",
        realtime: {
          delay: 1000,
          onRefresh: (chart) => {
            if (visible.current) {
              chart.data.datasets.forEach((i) => {
                i.hidden = i.label !== visible.current;
              });
            }
          },
        },
      },
    },
  };

  useEffect(() => {
    ws.current = new WebSocket("ws://0.0.0.0:8082/ws/");
    ws.current.onopen = () => console.log("Соединение открыто"); 
    ws.current.onclose = () => console.log("Соединение закрыто");
    gettingData();
  });

  const gettingData = () => {
    if (!ws.current) {
      return
    };

    ws.current.onmessage = (e) => {
      let message = JSON.parse(e.data);
      let keys = Object.keys(message);

      if (items.length === 0) {
        let obs = keys.map((i) => ({
          label: i,
          backgroundColor: "#" + (((1 << 24) * Math.random()) | 0).toString(16),
          borderColor: "#" + (((1 << 24) * Math.random()) | 0).toString(16),
          lineTension: 0,
          fill: false,
          cubicInterpolationMode: "monotone",
          data: [
            {
              x: Date.now(),
              y: message[i],
            },
          ],
        }));
        setItems(obs);
      } else {
        items.forEach((i) => i.data.push({ x: Date.now(), y: message[i.label] }));
        setItems(items);
      }
    };
  };

  var selectLine = (e) => {
    visible.current = e.target.value;
  };

  return (
    <div>
      <FormControl fullWidth sx={{ mt: "3%", mb: "2%" }}>
        <InputLabel id="demo-simple-select-label">Инструмент</InputLabel>
        <Select onChange={selectLine} label="Выберите инструмент">
          {items.map(i => i.label).map((i) => (
            <MenuItem value={i}> {i}</MenuItem>
          ))}
        </Select>
      </FormControl>

      <Line data={{ datasets: items }} options={options} />
    </div>
  );
};

export default App;
