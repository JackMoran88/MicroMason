export default function formattedPrice(value) {
  try {
    const parts = value.toString().split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    return parts.join('.');
  } catch (e) {
    return value;
  }
}
