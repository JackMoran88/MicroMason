export default function formattedDate(value) {
  const options = {
    year: '2-digit',
    month: 'numeric',
    day: 'numeric',
    timezone: 'UTC',
    hour: 'numeric',
    minute: 'numeric',
  };
  const parts = new Date(value).toLocaleTimeString('ru', options);
  return parts;
}
