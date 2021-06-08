export default function formattedDate(value) {
  const options = {
    year: '2-digit',
    month: 'numeric',
    day: 'numeric',
    timezone: 'UTC',
    hour: 'numeric',
    minute: 'numeric',
  };
  return new Date(value).toLocaleTimeString('ru', options);
}
